<script lang="ts" setup>
import { computed } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { TableSecondary } from '@/utils/cssMixins'
import Pagination from '@/components/Pagination'
import Contract from '@/views/contracts/List/components/Contract.vue'

const emit = defineEmits(['page-select'])

const contractStore = useContract()
const contractList = computed(() => contractStore.contractList)

const contractPages = (pageNum: number) => contractStore.contractPages(pageNum)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col style="width: 6%" />
      <col style="width: 6%" />
      <col style="width: 6%" />
      <col style="width: 5%" />
      <col style="width: 7%" />
      <col style="width: 8%" />
      <col style="width: 8%" />
      <col style="width: 8%" />
      <col style="width: 9%" />
      <col style="width: 8%" />
      <col style="width: 10%" />
      <col style="width: 8%" />
      <col style="width: 6%" />
      <col style="width: 5%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="TableSecondary" class="text-center">
        <CTableHeaderCell scope="col">일련번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록상태</CTableHeaderCell>
        <CTableHeaderCell scope="col">차수</CTableHeaderCell>
        <CTableHeaderCell scope="col">타입</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약자</CTableHeaderCell>
        <CTableHeaderCell scope="col">동호수</CTableHeaderCell>
        <CTableHeaderCell scope="col">가입 계약일</CTableHeaderCell>
        <CTableHeaderCell scope="col">공급 계약일</CTableHeaderCell>
        <CTableHeaderCell scope="col">공급계약가격</CTableHeaderCell>
        <CTableHeaderCell scope="col">회당 계약금</CTableHeaderCell>
        <CTableHeaderCell scope="col">최종납입회차</CTableHeaderCell>
        <CTableHeaderCell scope="col">납입금액합계</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약서</CTableHeaderCell>
        <CTableHeaderCell scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Contract v-for="contract in contractList" :key="contract.pk" :contract="contract" />
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="contractPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
