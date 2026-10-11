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
  ) => {
    try {
      const payload: Record<string, any> = {}
      if (customAccountId) payload.custom_account_id = customAccountId
      if (customContractId) payload.custom_contract_id = customContractId

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

  const syncAllCredentials = async (startDate?: string, endDate?: string) => {
    isLoading.value = true
    try {
      const payload: Record<string, any> = {}
      if (startDate) payload.start_date = startDate
      if (endDate) payload.end_date = endDate

      const res = await api.post('/ledger/credentials/sync_all/', payload)
      const { total_accounts, success_accounts, total_created, total_skipped } = res.data
      message(
        'success',
        '알림',
        `전체 계좌 수집 완료: 총 ${total_accounts}개 계좌 중 ${success_accounts}개 성공 (신규 ${total_created}건, 기존 중복 ${total_skipped}건)`,
      )
      return res.data
    } catch (err: any) {
      errorHandle(err.response?.data)
      throw err
    } finally {
      isLoading.value = false
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
  }
})
