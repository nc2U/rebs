import json
import logging
import re
from typing import Any, Dict, List, Optional

import requests
from django.conf import settings
from django.db.models import Count

from contract.models import Contract
from ledger.models import (
    CompanyAccount, ProjectAccount,
    CompanyAccountingEntry, ProjectAccountingEntry,
    RawBankTransaction
)

logger = logging.getLogger(__name__)


class TransactionClassifier:
    """
    은행 수집 거래(RawBankTransaction)에 대한 3단계 잠정 회계계정 분류기
    
    1단계: 건설 도메인 룰 엔진 (분양계약 동호수 파싱, 금융수수료/이자 감지) - 95~98%
    2단계: 과거 이력 패턴 매칭 (최근 6개월 동일 거래처/적요 기반) - 90%
    3단계: Google Gemini LLM 지능형 추론 (모호한 지출 적요 대상) - 70~85%
    """

    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"

    def __init__(self):
        self.gemini_api_key = getattr(settings, 'GEMINI_API_KEY', '')

    def classify(self, raw_tx: RawBankTransaction) -> Dict[str, Any]:
        """
        단일 RawBankTransaction을 3단계 파이프라인을 거쳐 분류
        """
        is_project = raw_tx.credential.is_project

        # --- 1단계: 룰 기반 매칭 ---
        rule_result = self._match_by_rules(raw_tx, is_project)
        if rule_result:
            return rule_result

        # --- 2단계: 과거 이력 패턴 매칭 ---
        history_result = self._match_by_history(raw_tx, is_project)
        if history_result:
            return history_result

        # --- 3단계: LLM(Gemini) 지능형 추론 ---
        if self.gemini_api_key:
            llm_result = self._match_by_llm(raw_tx, is_project)
            if llm_result:
                return llm_result

        # 매칭 실패 시 기본값
        return {
            'suggested_company_account': None,
            'suggested_project_account': None,
            'suggested_contract': None,
            'confidence_score': 0,
            'ai_reason': '매칭되는 규칙 또는 이력이 없어 담당자 지정이 필요합니다.',
            'matched_stage': 'none'
        }

    # -------------------------------------------------------------
    # 1단계: 룰 기반 매칭
    # -------------------------------------------------------------
    def _match_by_rules(self, raw_tx: RawBankTransaction, is_project: bool) -> Optional[Dict[str, Any]]:
        client_name = (raw_tx.client_name or '').strip()
        content = (raw_tx.content or '').strip()
        full_text = f"{client_name} {content}".strip()

        # (1) 이체수수료 탐지 (출금 거래)
        if raw_tx.sort_type == 'withdraw':
            fee_keywords = ['수수료', '이체수수료', '타행이체', '송금수수료', '펌뱅킹수수료']
            if any(k in full_text for k in fee_keywords):
                if is_project:
                    fee_acc = ProjectAccount.objects.filter(is_transfer_fee=True, is_active=True).first()
                    if fee_acc:
                        return {
                            'suggested_company_account': None,
                            'suggested_project_account': fee_acc,
                            'suggested_contract': None,
                            'confidence_score': 95,
                            'ai_reason': '은행 이체수수료 키워드 패턴 일치',
                            'matched_stage': 'rule'
                        }
                else:
                    fee_acc = CompanyAccount.objects.filter(is_transfer_fee=True, is_active=True).first()
                    if fee_acc:
                        return {
                            'suggested_company_account': fee_acc,
                            'suggested_project_account': None,
                            'suggested_contract': None,
                            'confidence_score': 95,
                            'ai_reason': '은행 이체수수료 키워드 패턴 일치',
                            'matched_stage': 'rule'
                        }

        # (2) 예금 결산이자 탐지 (입금 거래)
        if raw_tx.sort_type == 'deposit':
            interest_keywords = ['결산이자', '예금이자', '이자수익']
            if any(k in full_text for k in interest_keywords):
                if is_project:
                    int_acc = ProjectAccount.objects.filter(name__icontains='이자', category='revenue', is_active=True).first()
                    if int_acc:
                        return {
                            'suggested_company_account': None,
                            'suggested_project_account': int_acc,
                            'suggested_contract': None,
                            'confidence_score': 95,
                            'ai_reason': '예금 결산이자 수익 키워드 패턴 일치',
                            'matched_stage': 'rule'
                        }
                else:
                    int_acc = CompanyAccount.objects.filter(name__icontains='이자', category='revenue', is_active=True).first()
                    if int_acc:
                        return {
                            'suggested_company_account': int_acc,
                            'suggested_project_account': None,
                            'suggested_contract': None,
                            'confidence_score': 95,
                            'ai_reason': '예금 결산이자 수익 키워드 패턴 일치',
                            'matched_stage': 'rule'
                        }

        # (3) 분양대금 수납 매칭 (프로젝트 계좌 + 입금 거래)
        if is_project and raw_tx.sort_type == 'deposit':
            project = raw_tx.credential.project_bank_account.project
            contract, reason, confidence = self._match_contract_by_text(project, full_text, client_name)
            if contract:
                payment_acc = ProjectAccount.objects.filter(
                    is_payment=True, is_active=True, is_category_only=False
                ).first()
                return {
                    'suggested_company_account': None,
                    'suggested_project_account': payment_acc,
                    'suggested_contract': contract,
                    'confidence_score': confidence,
                    'ai_reason': reason,
                    'matched_stage': 'rule'
                }

        return None

    def _match_contract_by_text(self, project, full_text: str, client_name: str):
        """텍스트에서 동호수 또는 계약자명을 추출하여 Contract 매칭"""
        # 정규식 패턴: 101-1002 또는 101동 1002호
        unit_pattern = re.compile(r'(\d{2,4})[-동\s]+(\d{2,4})[호]?')
        match = unit_pattern.search(full_text)
        if match:
            dong = match.group(1).lstrip('0') or match.group(1)
            ho = match.group(2).lstrip('0') or match.group(2)

            contracts = Contract.objects.filter(
                project=project,
                key_unit__houseunit__building_unit__name__in=[dong, match.group(1)],
                key_unit__houseunit__name__in=[ho, match.group(2)]
            ).select_related('contractor', 'key_unit')

            if contracts.count() == 1:
                c = contracts.first()
                contractor_name = c.contractor.name if hasattr(c, 'contractor') and c.contractor else ''
                return c, f"분양계약 동호수({dong}동 {ho}호) 및 계약자({contractor_name}) 일치", 98
            elif contracts.count() > 1:
                # 계약자 이름으로 2차 필터
                for c in contracts:
                    if hasattr(c, 'contractor') and c.contractor and c.contractor.name in full_text:
                        return c, f"동호수({dong}동 {ho}호) 및 입금자명({c.contractor.name}) 일치", 98
                return contracts.first(), f"동호수({dong}동 {ho}호) 일치 (동일 동호수 다수 중 1순위)", 90

        # 이름만으로 검색 (동호수가 없는 입금)
        if client_name and len(client_name) >= 2:
            clean_name = re.sub(r'[^가-힣a-zA-Z]', '', client_name)
            if clean_name:
                name_contracts = Contract.objects.filter(
                    project=project,
                    contractor__name=clean_name
                ).select_related('contractor', 'key_unit')
                if name_contracts.count() == 1:
                    c = name_contracts.first()
                    unit_str = str(c.key_unit) if c.key_unit else ''
                    return c, f"계약자 성명({clean_name}) 단일 계약 일치 ({unit_str})", 85

        return None, "", 0

    # -------------------------------------------------------------
    # 2단계: 과거 이력 패턴 매칭
    # -------------------------------------------------------------
    def _match_by_history(self, raw_tx: RawBankTransaction, is_project: bool) -> Optional[Dict[str, Any]]:
        target_name = (raw_tx.client_name or raw_tx.content or '').strip()
        if not target_name or len(target_name) < 2:
            return None

        if is_project:
            project = raw_tx.credential.project_bank_account.project
            past_entries = (
                ProjectAccountingEntry.objects.filter(project=project, trader__icontains=target_name)
                .values('account')
                .annotate(count=Count('id'))
                .order_by('-count')
            )
            if past_entries.exists():
                best_account_id = past_entries.first()['account']
                acc = ProjectAccount.objects.filter(id=best_account_id, is_active=True).first()
                if acc:
                    return {
                        'suggested_company_account': None,
                        'suggested_project_account': acc,
                        'suggested_contract': None,
                        'confidence_score': 90,
                        'ai_reason': f"과거 동일 거래처('{target_name}') {past_entries.first()['count']}회 승인 이력 일치",
                        'matched_stage': 'history'
                    }
        else:
            company = raw_tx.credential.company_bank_account.company
            past_entries = (
                CompanyAccountingEntry.objects.filter(company=company, trader__icontains=target_name)
                .values('account')
                .annotate(count=Count('id'))
                .order_by('-count')
            )
            if past_entries.exists():
                best_account_id = past_entries.first()['account']
                acc = CompanyAccount.objects.filter(id=best_account_id, is_active=True).first()
                if acc:
                    return {
                        'suggested_company_account': acc,
                        'suggested_project_account': None,
                        'suggested_contract': None,
                        'confidence_score': 90,
                        'ai_reason': f"과거 동일 거래처('{target_name}') {past_entries.first()['count']}회 승인 이력 일치",
                        'matched_stage': 'history'
                    }

        return None

    # -------------------------------------------------------------
    # 3단계: Gemini LLM 지능형 추론
    # -------------------------------------------------------------
    def _match_by_llm(self, raw_tx: RawBankTransaction, is_project: bool) -> Optional[Dict[str, Any]]:
        # 계정과목 후보군 텍스트 생성
        if is_project:
            accounts = list(ProjectAccount.objects.filter(is_active=True, is_category_only=False).values('code', 'name', 'category', 'direction'))
        else:
            accounts = list(CompanyAccount.objects.filter(is_active=True, is_category_only=False).values('code', 'name', 'category', 'direction'))

        if not accounts:
            return None

        account_list_text = "\n".join([f"- 코드: {a['code']}, 계정명: {a['name']} ({a['category']}, {a['direction'] or '양방향'})" for a in accounts[:50]])

        prompt = f"""
당신은 대한민국 건설 시행/시공 회사의 최고 회계 전문가입니다.
아래 주어진 은행 통장 입출금 거래내역을 분석하여, 제시된 회계 계정과목 목록 중 가장 적합한 계정과목 1개를 추천해 주세요.

[거래 정보]
- 거래일자: {raw_tx.deal_date}
- 입출금구분: {raw_tx.get_sort_type_display()} ({raw_tx.sort_type})
- 거래금액: {raw_tx.amount:,}원
- 거래처/입금자명: {raw_tx.client_name}
- 통장 적요: {raw_tx.content}
- 취급점: {raw_tx.branch_name}

[사용 가능한 계정과목 목록]
{account_list_text}

반드시 아래 JSON 형식으로만 응답해 주세요:
{{
  "recommended_code": "선택한 계정코드 (예: 5010)",
  "confidence_score": 75,
  "reason": "해당 계정과목으로 추천한 명확한 회계적 사유 (한 문장)"
}}
"""

        candidate_models = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
        for model_name in candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.gemini_api_key}"
            headers = {"Content-Type": "application/json"}
            body = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "response_mime_type": "application/json",
                    "temperature": 0.1
                }
            }

            try:
                resp = requests.post(url, json=body, headers=headers, timeout=15)
                if not resp.ok:
                    logger.warning("Gemini LLM [%s] 호출 실패 (%d): %s", model_name, resp.status_code, resp.text)
                    continue

                result_json = resp.json()
                candidates = result_json.get('candidates', [])
                if not candidates:
                    continue

                raw_text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                parsed = json.loads(raw_text)

                rec_code = str(parsed.get('recommended_code', '')).strip()
                confidence = int(parsed.get('confidence_score', 75))
                reason = parsed.get('reason', 'AI 분석 추천')

                if is_project:
                    acc = ProjectAccount.objects.filter(code=rec_code, is_active=True).first()
                    if acc:
                        return {
                            'suggested_company_account': None,
                            'suggested_project_account': acc,
                            'suggested_contract': None,
                            'confidence_score': min(confidence, 85),  # LLM은 최대 85%로 상한 설정
                            'ai_reason': f"[AI 추론] {reason}",
                            'matched_stage': 'llm'
                        }
                else:
                    acc = CompanyAccount.objects.filter(code=rec_code, is_active=True).first()
                    if acc:
                        return {
                            'suggested_company_account': acc,
                            'suggested_project_account': None,
                            'suggested_contract': None,
                            'confidence_score': min(confidence, 85),
                            'ai_reason': f"[AI 추론] {reason}",
                            'matched_stage': 'llm'
                        }

            except Exception as e:
                logger.warning("Gemini [%s] 분류 중 예외 발생: %s", model_name, str(e))
                continue

        return None


def classify_single_raw_transaction(raw_tx: RawBankTransaction) -> RawBankTransaction:
    """단일 RawBankTransaction 분류 실행 및 DB 업데이트"""
    classifier = TransactionClassifier()
    result = classifier.classify(raw_tx)

    raw_tx.suggested_company_account = result['suggested_company_account']
    raw_tx.suggested_project_account = result['suggested_project_account']
    raw_tx.suggested_contract = result['suggested_contract']
    raw_tx.confidence_score = result['confidence_score']
    raw_tx.ai_reason = result['ai_reason']
    raw_tx.status = 'ready'  # 분류 완료 -> 담당자 컨펌 대기

    raw_tx.save(update_fields=[
        'suggested_company_account',
        'suggested_project_account',
        'suggested_contract',
        'confidence_score',
        'ai_reason',
        'status',
        'updated_at'
    ])
    return raw_tx


def classify_pending_raw_transactions(limit: int = 50) -> Dict[str, Any]:
    """미분류(pending) 상태의 거래내역들을 일괄 분류"""
    pending_list = RawBankTransaction.objects.filter(status='pending')[:limit]
    total = len(pending_list)
    classified_count = 0

    classifier = TransactionClassifier()

    for raw in pending_list:
        try:
            result = classifier.classify(raw)
            raw.suggested_company_account = result['suggested_company_account']
            raw.suggested_project_account = result['suggested_project_account']
            raw.suggested_contract = result['suggested_contract']
            raw.confidence_score = result['confidence_score']
            raw.ai_reason = result['ai_reason']
            raw.status = 'ready'
            raw.save(update_fields=[
                'suggested_company_account',
                'suggested_project_account',
                'suggested_contract',
                'confidence_score',
                'ai_reason',
                'status',
                'updated_at'
            ])
            classified_count += 1
        except Exception as e:
            logger.error("RawBankTransaction ID=%d 분류 실패: %s", raw.id, str(e))

    return {
        'total_pending': total,
        'classified_count': classified_count
    }
