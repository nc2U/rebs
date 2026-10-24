import logging
from typing import Any, Dict, List, Optional

from django.db import transaction
from django.utils import timezone

from ibs.models import AccountSort
from ledger.models import (
    CompanyAccountingEntry, CompanyBankTransaction,
    ProjectAccountingEntry, ProjectBankTransaction,
    RawBankTransaction
)

logger = logging.getLogger(__name__)


@transaction.atomic
def confirm_raw_transaction(
    raw_tx: RawBankTransaction,
    user=None,
    custom_account=None,
    custom_contract=None,
    entries_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    수집된 RawBankTransaction을 승인(Confirm)하여 정식 원장 및 분양수납(payment)으로 반영
    (단일 분개 및 복합 거래 복수 분개 분할 지원)
    
    Args:
        raw_tx: 승인할 RawBankTransaction 인스턴스
        user: 승인자 (User 인스턴스)
        custom_account: 담당자가 직접 변경/선택한 회계계정 (단일 분개 시)
        custom_contract: 담당자가 직접 변경/선택한 분양계약 (단일 분개 시)
        entries_data: 복수 분개 항목 리스트 [{'account': ..., 'amount': ..., 'trader': ..., 'contract': ...}, ...]
    
    Returns:
        Dict: 생성된 거래 및 분개 정보
    """
    # 비관적 락(Pessimistic Lock)을 획득하여 동시 중복 승인 및 이중 분개 원천 차단
    raw_tx = RawBankTransaction.objects.select_for_update().get(pk=raw_tx.pk)
    if raw_tx.status == 'confirmed':
        raise ValueError(f"RawBankTransaction #{raw_tx.id}는 이미 승인 완료된 거래입니다.")

    cred = raw_tx.credential
    is_project = cred.is_project

    # 1. 입금(1)/출금(2) sort 매핑
    sort_id = 1 if raw_tx.sort_type == 'deposit' else 2
    sort_obj = AccountSort.objects.get(id=sort_id)

    # 2. 분개 데이터 검증 및 준비
    if entries_data and len(entries_data) > 0:
        total_entry_amount = sum(item['amount'] for item in entries_data)
        if total_entry_amount != raw_tx.amount:
            raise ValueError(
                f"분개 금액 합계({total_entry_amount:,}원)가 통장 거래금액({raw_tx.amount:,}원)과 일치하지 않습니다. (차액: {raw_tx.amount - total_entry_amount:,}원)"
            )
        resolved_entries = entries_data
    else:
        # 단일 분개 기본 처리
        account = custom_account or (raw_tx.suggested_project_account if is_project else raw_tx.suggested_company_account)
        if not account:
            raise ValueError("회계 계정과목이 지정되지 않았습니다. 계정을 선택해 주세요.")
        contract = custom_contract or raw_tx.suggested_contract if is_project else None
        resolved_entries = [{
            'account': account,
            'amount': raw_tx.amount,
            'trader': raw_tx.client_name or '',
            'contract': contract
        }]

    # 3. 프로젝트 거래 생성
    if is_project:
        project_bank_acc = cred.project_bank_account
        project = project_bank_acc.project

        # (1) ProjectBankTransaction 생성
        bank_tx = ProjectBankTransaction.objects.create(
            project=project,
            bank_account=project_bank_acc,
            deal_date=raw_tx.deal_date,
            sort=sort_obj,
            amount=raw_tx.amount,
            content=raw_tx.content or raw_tx.client_name or '은행 거래',
            note=f"자동수집승인 (취급점: {raw_tx.branch_name})" if raw_tx.branch_name else "자동수집승인",
            creator=user,
            updator=user
        )

        # (2) ProjectAccountingEntry 복수/단수 생성 (save 시 내부에서 trigger_sync_contract_payment 동작)
        created_entry_ids = []
        for e in resolved_entries:
            c = e.get('contract')
            contractor = c.contractor if c and hasattr(c, 'contractor') else None
            entry_trader = e.get('trader') or raw_tx.client_name or (contractor.name if contractor else '')
            entry = ProjectAccountingEntry.objects.create(
                project=project,
                transaction_id=bank_tx.transaction_id,
                account=e['account'],
                amount=e['amount'],
                trader=entry_trader,
                contract=c,
                contractor=contractor
            )
            created_entry_ids.append(entry.id)

        # (3) RawBankTransaction 상태 업데이트
        raw_tx.status = 'confirmed'
        raw_tx.confirmed_by = user
        raw_tx.confirmed_at = timezone.now()
        raw_tx.created_project_transaction = bank_tx
        raw_tx.save(update_fields=[
            'status', 'confirmed_by', 'confirmed_at',
            'created_project_transaction', 'updated_at'
        ])

        logger.info(
            "RawBankTransaction #%d 승인 완료 -> ProjectBankTransaction #%d, ProjectAccountingEntry %s 생성",
            raw_tx.id, bank_tx.id, created_entry_ids
        )

        return {
            'success': True,
            'bank_transaction_id': bank_tx.id,
            'accounting_entry_id': created_entry_ids[0] if created_entry_ids else None,
            'accounting_entry_ids': created_entry_ids,
            'is_project': True
        }

    # 4. 본사 거래 생성
    else:
        com_bank_acc = cred.company_bank_account
        company = com_bank_acc.company

        # (1) CompanyBankTransaction 생성
        bank_tx = CompanyBankTransaction.objects.create(
            company=company,
            bank_account=com_bank_acc,
            deal_date=raw_tx.deal_date,
            sort=sort_obj,
            amount=raw_tx.amount,
            content=raw_tx.content or raw_tx.client_name or '은행 거래',
            note=f"자동수집승인 (취급점: {raw_tx.branch_name})" if raw_tx.branch_name else "자동수집승인",
            creator=user,
            updator=user
        )

        # (2) CompanyAccountingEntry 복수/단수 생성
        created_entry_ids = []
        for e in resolved_entries:
            entry_trader = e.get('trader') or raw_tx.client_name or ''
            entry = CompanyAccountingEntry.objects.create(
                company=company,
                transaction_id=bank_tx.transaction_id,
                account=e['account'],
                amount=e['amount'],
                trader=entry_trader
            )
            created_entry_ids.append(entry.id)

        # (3) RawBankTransaction 상태 업데이트
        raw_tx.status = 'confirmed'
        raw_tx.confirmed_by = user
        raw_tx.confirmed_at = timezone.now()
        raw_tx.created_company_transaction = bank_tx
        raw_tx.save(update_fields=[
            'status', 'confirmed_by', 'confirmed_at',
            'created_company_transaction', 'updated_at'
        ])

        logger.info(
            "RawBankTransaction #%d 승인 완료 -> CompanyBankTransaction #%d, CompanyAccountingEntry %s 생성",
            raw_tx.id, bank_tx.id, created_entry_ids
        )

        return {
            'success': True,
            'bank_transaction_id': bank_tx.id,
            'accounting_entry_id': created_entry_ids[0] if created_entry_ids else None,
            'accounting_entry_ids': created_entry_ids,
            'is_project': False
        }


def bulk_confirm_high_confidence(user=None, min_confidence: int = 90, base_qs=None) -> Dict[str, Any]:
    """
    신뢰도가 기준점(기본 90%) 이상인 대기 상태 거래들을 일괄 승인
    """
    targets = base_qs if base_qs is not None else RawBankTransaction.objects.all()
    targets = targets.filter(
        status='ready',
        confidence_score__gte=min_confidence
    )

    total = targets.count()
    success_count = 0
    errors = []

    for raw in targets:
        try:
            confirm_raw_transaction(raw, user=user)
            success_count += 1
        except Exception as e:
            errors.append(f"#{raw.id}: 승인 처리 중 오류가 발생했습니다.")
            logger.error("일괄 승인 중 #%d 실패: %s", raw.id, str(e))

    return {
        'total_targets': total,
        'success_count': success_count,
        'error_count': len(errors),
        'errors': errors
    }
