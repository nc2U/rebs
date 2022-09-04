<script lang="ts" setup>
import { computed } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { headerSecondary } from '@/utils/cssMixins'
import Pagination from '@/components/Pagination'
import Contract from '@/views/contracts/List/components/Contract.vue'

const emit = defineEmits(['page-select'])

const contractStore = useContract()
const contractIndex = computed(() => contractStore.contractIndex)

const contractPages = (pageNum: number) => contractStore.contractPages(pageNum)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="8%" />
      <col width="8%" />
      <col width="7%" />
      <col width="7%" />
      <col width="8%" />
      <col width="9%" />
      <col width="9%" />
      <col width="6%" />
      <col width="15%" />
      <col width="10%" />
      <col width="10%" />
      <col width="3%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="headerSecondary" class="text-center">
        <CTableHeaderCell scope="col">일련번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">차수</CTableHeaderCell>
        <CTableHeaderCell scope="col">타입</CTableHeaderCell>
        <CTableHeaderCell scope="col">동호수</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약자</CTableHeaderCell>
        <CTableHeaderCell scope="col">최종납입회차</CTableHeaderCell>
        <CTableHeaderCell scope="col">납입금액합계</CTableHeaderCell>
        <CTableHeaderCell scope="col">인가 등록여부</CTableHeaderCell>
        <CTableHeaderCell scope="col">주소</CTableHeaderCell>
        <CTableHeaderCell scope="col">연락처</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약일자</CTableHeaderCell>
        <CTableHeaderCell scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Contract
        v-for="contract in contractIndex"
        :key="contract.pk"
        :contract="contract"
      />
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
