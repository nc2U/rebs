import datetime
import logging
from typing import Any, Dict, List, Optional

from django.db import transaction
from django.utils import timezone

from ledger.models import BankApiCredential, RawBankTransaction
from ledger.services.codef_client import CodefClient, CodefException

logger = logging.getLogger(__name__)


def sync_credential_transactions(
    credential: BankApiCredential,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    is_sandbox: bool = False
) -> Dict[str, Any]:
    """
    특정 연동 계좌의 거래내역을 CODEF로부터 수집하여 RawBankTransaction에 적재
    
    Args:
        credential: 연동 계좌 모델 인스턴스
        start_date: 조회 시작일 (YYYYMMDD, 기본값: 어제)
        end_date: 조회 종료일 (YYYYMMDD, 기본값: 오늘)
        is_sandbox: 샌드박스 호출 여부
    
    Returns:
        Dict: {'total': int, 'created': int, 'skipped': int, 'errors': List[str]}
    """
    today = timezone.localdate()
    yesterday = today - datetime.timedelta(days=1)

    s_date = start_date or yesterday.strftime('%Y%m%d')
    e_date = end_date or today.strftime('%Y%m%d')

    client = CodefClient(is_sandbox=is_sandbox)

    stats = {
        'total': 0,
        'created': 0,
        'skipped': 0,
        'errors': []
    }
    created_raw_txs = []

    try:
        if credential.auth_type == 'fast':
            # 빠른조회 (신탁사/조합 계좌: connectedId 없이 사업자번호+비밀번호로 즉시 조회)
            raw_list = client.fetch_fast_transactions(
                organization=credential.bank_code,
                account_number=credential.account_number,
                start_date=s_date,
                end_date=e_date,
                account_password=credential.fast_password,
                identity=credential.fast_business_number,
                is_business=True
            )
        else:
            # 일반 공동인증서/아이디 연동 (connectedId 기반)
            raw_list = client.fetch_transactions(
                connected_id=credential.connected_id,
                organization=credential.bank_code,
                account_number=credential.account_number,
                start_date=s_date,
                end_date=e_date,
                is_business=True  # 기본 법인
            )
    except CodefException as ce:
        error_msg = f"CODEF API 실패 [{ce.code}]: {ce.message}"
        logger.error("계좌 %s 수집 오류: %s", credential.account_number, error_msg)
        credential.last_status = 'error'
        credential.last_error_message = error_msg
        credential.save(update_fields=['last_status', 'last_error_message', 'updated_at'])
        stats['errors'].append(error_msg)
        return stats
    except Exception as e:
        error_msg = f"수집 중 알 수 없는 예외: {str(e)}"
        logger.exception("계좌 %s 수집 예외 발생", credential.account_number)
        credential.last_status = 'error'
        credential.last_error_message = error_msg
        credential.save(update_fields=['last_status', 'last_error_message', 'updated_at'])
        stats['errors'].append(error_msg)
        return stats

    stats['total'] = len(raw_list)

    for item in raw_list:
        try:
            # 1. 거래일시 파싱
            date_str = item.get('resAccountTrDate', '')
            if not date_str or len(date_str) != 8:
                continue
            deal_date = datetime.datetime.strptime(date_str, '%Y%m%d').date()

            time_str = item.get('resAccountTrTime', '')
            deal_time = None
            if time_str and len(time_str) >= 6:
                try:
                    deal_time = datetime.datetime.strptime(time_str[:6], '%H%M%S').time()
                except ValueError:
                    deal_time = None

            # 2. 금액 및 입출금 구분
            in_amt = int(item.get('resAccountIn', 0) or 0)
            out_amt = int(item.get('resAccountOut', 0) or 0)

            if in_amt > 0:
                sort_type = 'deposit'
                amount = in_amt
            else:
                sort_type = 'withdraw'
                amount = out_amt

            if amount <= 0:
                continue

            balance_raw = item.get('resAfterTranBalance') or item.get('resAccountBalance')
            balance = int(balance_raw) if balance_raw is not None and str(balance_raw).isdigit() else None

            # 3. 텍스트 정보 매핑
            # CODEF는 은행별로 desc1~desc4에 거래처, 적요, 통장표시내용을 다르게 채움
            desc1 = (item.get('resAccountDesc1') or '').strip()
            desc2 = (item.get('resAccountDesc2') or '').strip()
            desc3 = (item.get('resAccountDesc3') or '').strip()
            desc4 = (item.get('resAccountDesc4') or '').strip()

            content = desc2 or desc1 or '은행 거래'
            client_name = desc3 or desc1 or ''
            branch_name = desc4

            # 4. 고유 식별 해시 생성 (Idempotency)
            tx_hash = RawBankTransaction.generate_hash(
                account_no=credential.account_number,
                date=deal_date,
                time=deal_time,
                sort_type=sort_type,
                amount=amount,
                balance=balance,
                client_name=client_name,
                content=content
            )

            # 5. DB 저장 (이미 존재하면 Skip)
            with transaction.atomic():
                obj, created = RawBankTransaction.objects.get_or_create(
                    tx_hash=tx_hash,
                    defaults={
                        'credential': credential,
                        'deal_date': deal_date,
                        'deal_time': deal_time,
                        'sort_type': sort_type,
                        'amount': amount,
                        'balance': balance,
                        'client_name': client_name,
                        'content': content,
                        'branch_name': branch_name,
                        'raw_data': item,
                        'status': 'pending'
                    }
                )

                if created:
                    stats['created'] += 1
                    created_raw_txs.append(obj)
                else:
                    stats['skipped'] += 1

        except Exception as ex:
            logger.warning("거래 파싱 에러 (%s): %s", item, str(ex))
            stats['errors'].append(str(ex))

    # 신규 수집된 거래에 대해 AI 잠정 계정 분류 자동 실행
    if created_raw_txs:
        try:
            from ledger.services.ai_classifier import classify_single_raw_transaction
            for r_tx in created_raw_txs:
                classify_single_raw_transaction(r_tx)
            logger.info("신규 수집 %d건에 대한 AI 계정 분류 완료", len(created_raw_txs))
        except Exception as ce:
            logger.error("AI 분류 실행 중 오류: %s", str(ce))

    # 계좌 수집 상태 성공 갱신
    credential.last_scraped_at = timezone.now()
    credential.last_status = 'success'
    credential.last_error_message = ''
    credential.save(update_fields=['last_scraped_at', 'last_status', 'last_error_message', 'updated_at'])

    logger.info(
        "계좌 %s 수집 완료: 총 %d건 중 신규 %d건, 스킵 %d건",
        credential.account_number, stats['total'], stats['created'], stats['skipped']
    )
    return stats


def sync_all_active_credentials(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    credential_ids: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    활성화된 연동 계좌를 순회하며 거래내역 자동 수집
    credential_ids가 주어지면 해당 계좌들만 타겟팅하여 수집 (API 호출 수 최적화)
    """
    credentials = BankApiCredential.objects.filter(is_active=True)
    if credential_ids:
        credentials = credentials.filter(pk__in=credential_ids)

    summary = {
        'total_accounts': credentials.count(),
        'success_accounts': 0,
        'total_created': 0,
        'total_skipped': 0,
        'details': []
    }

    for cred in credentials:
        res = sync_credential_transactions(cred, start_date=start_date, end_date=end_date)
        if cred.last_status == 'success':
            summary['success_accounts'] += 1
        summary['total_created'] += res['created']
        summary['total_skipped'] += res['skipped']
        summary['details'].append({
            'account': str(cred),
            'stats': res
        })

    return summary
