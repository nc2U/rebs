import api from '@/api'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
import type {
  BankApiCredential,
  RawBankTransaction,
  RawTransactionFilter,
} from '@/store/types/rawTransaction'

export const useRawTransaction = defineStore('rawTransaction', () => {
  // State
  const rawTransList = ref<RawBankTransaction[]>([])
  const rawTransCount = ref<number>(0)
  const credentialList = ref<BankApiCredential[]>([])
  const isLoading = ref<boolean>(false)

  // Actions
  const fetchCredentialList = async (params: Record<string, any> = {}) => {
    try {
      const res = await api.get('/ledger/credentials/', { params })
      credentialList.value = res.data.results || res.data
    } catch (err: any) {
      errorHandle(err.response?.data)
    }
  }

  const fetchRawTransList = async (filters: RawTransactionFilter = {}) => {
    isLoading.value = true
    try {
      const res = await api.get('/ledger/raw-transactions/', { params: filters })
      rawTransList.value = res.data.results || res.data
      rawTransCount.value = res.data.count || rawTransList.value.length
    } catch (err: any) {
      errorHandle(err.response?.data)
    } finally {
      isLoading.value = false
    }
  }

  const confirmRawTransaction = async (
    pk: number,
    customAccountId?: number | null,
    customContractId?: number | null,
    entries?: Array<{
      account_id: number
      amount: number
      trader?: string
      contract_id?: number | null
    }> | null,
  ) => {
    try {
      const payload: Record<string, any> = {}
      if (customAccountId) payload.custom_account_id = customAccountId
      if (customContractId) payload.custom_contract_id = customContractId
      if (entries && entries.length > 0) payload.entries = entries

      const res = await api.post(`/ledger/raw-transactions/${pk}/confirm/`, payload)
      message('success', '알림', '해당 거래가 정식 원장 및 분양수납으로 승인 반영되었습니다.')
      return res.data
    } catch (err: any) {
      errorHandle(err.response?.data)
      throw err
    }
  }

  const bulkConfirm = async (minConfidence = 90) => {
    try {
      const res = await api.post('/ledger/raw-transactions/bulk-confirm/', {
        min_confidence: minConfidence,
      })
      const { success_count, error_count } = res.data
      message(
        'success',
        '알림',
        `일괄 승인 완료: 성공 ${success_count}건${error_count > 0 ? `, 실패 ${error_count}건` : ''}`,
      )
      return res.data
    } catch (err: any) {
      errorHandle(err.response?.data)
      throw err
    }
  }

  const syncCredential = async (credPk: number, startDate?: string, endDate?: string) => {
    try {
      const payload: Record<string, any> = {}
      if (startDate) payload.start_date = startDate
      if (endDate) payload.end_date = endDate

      const res = await api.post(`/ledger/credentials/${credPk}/sync/`, payload)
      const { total, created, skipped } = res.data
      message(
        'success',
        '알림',
        `은행 거래 수집 완료: 총 ${total}건 (신규 ${created}건, 기존 중복 ${skipped}건)`,
      )
      return res.data
    } catch (err: any) {
      errorHandle(err.response?.data)
      throw err
    }
  }

  const syncAllCredentials = async (
    startDate?: string,
    endDate?: string,
    credentialIds?: number[],
  ) => {
    isLoading.value = true
    try {
      const payload: Record<string, any> = {}
      if (startDate) payload.start_date = startDate
      if (endDate) payload.end_date = endDate
      if (credentialIds && credentialIds.length > 0) payload.credential_ids = credentialIds

      const res = await api.post('/ledger/credentials/sync_all/', payload)
      const { total_accounts, success_accounts, total_created, total_skipped } = res.data
      if (total_accounts === 0) {
        message(
          'warning',
          '수집 안내',
          '수집 대상인 등록된 은행 연동 계좌가 없습니다. 먼저 [+ 새 계좌/인증서 연동] 버튼을 눌러 계좌를 등록해 주세요.',
        )
      } else {
        message(
          'success',
          '계좌 수집 완료',
          `계좌 수집 완료: 총 ${total_accounts}개 계좌 중 ${success_accounts}개 성공 (신규 ${total_created}건, 기존 중복 ${total_skipped}건)`,
        )
      }
      return res.data
    } catch (err: any) {
      errorHandle(err.response?.data)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const registerCertificate = async (formData: FormData): Promise<any> => {
    try {
      const res = await api.post('/ledger/credentials/register_certificate/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      const accCount = res.data.accounts?.length || 0
      if (accCount === 0) {
        message(
          'warning',
          '인증서 등록 알림',
          '공동인증서는 인증되었으나 해당 은행에서 조회된 보유 계좌가 0건입니다. 은행 및 인증서 등록 여부를 확인해 주세요.',
        )
      } else {
        message(
          'success',
          '인증서 등록 성공',
          `공동인증서 등록 완료: 은행에서 총 ${accCount}개의 보유 계좌를 확인했습니다. 연동할 계좌를 선택해 주세요.`,
        )
      }
      return res.data
    } catch (err: any) {
      errorHandle(err.response?.data)
      throw err
    }
  }

  const batchLinkCredentials = async (payload: any) => {
    try {
      const res = await api.post('/ledger/credentials/batch_link/', payload)
      message(
        'success',
        '계좌 연동 완료',
        `공동인증서 및 ${res.data.linked_count}개 계좌가 시스템에 정상 연동되었습니다.`,
      )
      await fetchCredentialList()
      return res.data
    } catch (err: any) {
      errorHandle(err.response?.data)
      throw err
    }
  }

  const registerFastAccount = async (payload: any) => {
    try {
      const res = await api.post('/ledger/credentials/register_fast_account/', payload)
      message('success', '신탁/빠른조회 연동 완료', res.data.message || '계좌가 성공적으로 연동되었습니다.')
      await fetchCredentialList()
      return res.data
    } catch (err: any) {
      errorHandle(err.response?.data)
      throw err
    }
  }

  return {
    rawTransList,
    rawTransCount,
    credentialList,
    isLoading,
    fetchCredentialList,
    fetchRawTransList,
    confirmRawTransaction,
    bulkConfirm,
    syncCredential,
    syncAllCredentials,
    registerCertificate,
    batchLinkCredentials,
    registerFastAccount,
  }
})

