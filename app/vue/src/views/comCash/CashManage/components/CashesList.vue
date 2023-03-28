<script lang="ts" setup>
import { computed } from 'vue'
import { useComCash } from '@/store/pinia/comCash'
import { CashBook } from '@/store/types/comCash'
import { TableSecondary } from '@/utils/cssMixins'
import Cashes from '@/views/comCash/CashManage/components/Cashes.vue'
import Pagination from '@/components/Pagination'
import AccDepth from './AccDepth.vue'
import BankAcc from './BankAcc.vue'

defineProps({ company: { type: Object, default: null } })

const emit = defineEmits([
  'page-select',
  'multi-submit',
  'on-delete',
  'patch-d3-hide',
  'patch-bank-hide',
])

const useComCashStore = useComCash()
const cashesPages = computed(() => useComCashStore.cashesPages)
const getCashLogs = computed(() => useComCashStore.getCashLogs)

const pageSelect = (page: number) => emit('page-select', page)

const multiSubmit = (payload: {
  formData: CashBook
  sepData: CashBook | null
}) => emit('multi-submit', payload)

const onDelete = (pk: number) => emit('on-delete', pk)

const patchD3Hide = (payload: { pk: number; is_hide: boolean }) =>
  emit('patch-d3-hide', payload)

const patchBankHide = (payload: any) => emit('patch-bank-hide', payload)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="8%" />
      <col width="5%" />
      <col width="5%" />
      <col width="9%" />
      <col width="15%" />
      <col width="11%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="11%" />
      <col width="6%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="TableSecondary" class="text-center">
        <CTableHeaderCell scope="col">거래일자</CTableHeaderCell>
        <CTableHeaderCell scope="col">구분</CTableHeaderCell>
        <CTableHeaderCell scope="col">계정</CTableHeaderCell>
        <CTableHeaderCell scope="col">
          세부계정
          <a href="javascript:void(0)">
            <CIcon name="cilCog" @click="$refs.accDepth.callModal()" />
          </a>
        </CTableHeaderCell>
        <CTableHeaderCell scope="col">적요</CTableHeaderCell>
        <CTableHeaderCell scope="col">거래처</CTableHeaderCell>
        <CTableHeaderCell scope="col">
          거래계좌
          <a href="javascript:void(0)">
            <CIcon name="cilCog" @click="$refs.bankAcc.callModal()" />
          </a>
        </CTableHeaderCell>
        <CTableHeaderCell scope="col">입금액</CTableHeaderCell>
        <CTableHeaderCell scope="col">출금액</CTableHeaderCell>
        <CTableHeaderCell scope="col">지출증빙</CTableHeaderCell>
        <CTableHeaderCell scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Cashes
        v-for="cash in getCashLogs"
        :key="cash.pk"
        :cash="cash"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @patchD3Hide="patchD3Hide"
      />
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="cashesPages(15)"
    class="mt-3"
    @active-page-change="pageSelect"
  />

  <AccDepth ref="accDepth" @patchD3Hide="patchD3Hide" />

  <BankAcc ref="bankAcc" @patchBankHide="patchBankHide" />
</template>
