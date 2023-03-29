<script lang="ts" setup>
import { computed } from 'vue'
import { useProCash } from '@/store/pinia/proCash'
import { ProjectCashBook } from '@/store/types/proCash'
import { TableSecondary } from '@/utils/cssMixins'
import ProCash from '@/views/proCash/Manage/components/ProCash.vue'
import Pagination from '@/components/Pagination'
import AccDepth from './AccDepth.vue'
import BankAcc from './BankAcc.vue'

const emit = defineEmits(['page-select', 'on-delete', 'multi-submit'])

const proCashStore = useProCash()
const proCashPages = computed(() => proCashStore.proCashPages)
const proCashBookList = computed(() => proCashStore.proCashBookList)

const pageSelect = (page: number) => emit('page-select', page)

const multiSubmit = (payload: {
  formData: ProjectCashBook
  sepData: ProjectCashBook | null
}) => emit('multi-submit', payload)

const onDelete = (payload: { project: number; pk: number }) =>
  emit('on-delete', payload)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="8%" />
      <col width="6%" />
      <col width="7%" />
      <col width="10%" />
      <col width="12%" />
      <col width="11%" />
      <col width="11%" />
      <col width="10%" />
      <col width="10%" />
      <col width="9%" />
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
      <ProCash
        v-for="proCash in proCashBookList"
        :key="proCash.pk"
        :pro-cash="proCash"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="proCashPages(15)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
  <AccDepth ref="accDepth" />

  <BankAcc ref="bankAcc" @onBankUpdate="onBankUpdate" />
</template>
