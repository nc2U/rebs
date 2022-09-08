import api from '@/api'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import { SalesBillIssue } from '@/store/types/notice'

export const useNotice = defineStore('notice', () => {
  // state & getters
  const billIssue = ref<SalesBillIssue | null>(null)

  // actions
  const fetchSalesBillIssue = (pk: number) =>
    api
      .get(`/sales-bill-issue/${pk}/`)
      .then(res => (billIssue.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createSalesBillIssue = (payload: SalesBillIssue) =>
    api
      .post('/sales-bill-issue/', payload)
      .then(() => message())
      .catch(err => errorHandle(err.response.data))

  const patchSalesBillIssue = (payload: SalesBillIssue) =>
    api
      .patch(`/sales-bill-issue/${payload.pk}/`, payload)
      .then(() => message())
      .catch(err => errorHandle(err.response.data))

  const updateSalesBillIssue = (payload: SalesBillIssue) =>
    api
      .put(`/sales-bill-issue/${payload.pk}/`, payload)
      .then(() => message())
      .catch(err => errorHandle(err.response.data))

  const deleteSalesBillIssue = (pk: number) =>
    api
      .delete(`/sales-bill-issue/${pk}/`)
      .then(() => message('warning', '', '해당 오브젝트가 삭제되었습니다.'))
      .catch(err => errorHandle(err.response.data))

  return {
    billIssue,

    fetchSalesBillIssue,
    createSalesBillIssue,
    patchSalesBillIssue,
    updateSalesBillIssue,
    deleteSalesBillIssue,
  }
})
