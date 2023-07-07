<script lang="ts" setup>
import { computed } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { Succession as SuccessType } from '@/store/types/contract'
import { TableSecondary } from '@/utils/cssMixins'
import Pagination from '@/components/Pagination'
import Succession from '@/views/contracts/Succession/components/Succession.vue'

const emit = defineEmits(['page-select', 'on-submit'])

const contractStore = useContract()
const successionList = computed(() => contractStore.successionList)
const successionPages = computed(() => contractStore.successionPages)

const pageSelect = (page: number) => emit('page-select', page)
const onSubmit = (payload: SuccessType) => emit('on-submit', payload)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="11%" />
      <col width="8%" />
    </colgroup>

    <CTableHead :color="TableSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>계약 정보</CTableHeaderCell>
        <CTableHeaderCell>양도계약자</CTableHeaderCell>
        <CTableHeaderCell>양수계약자</CTableHeaderCell>
        <CTableHeaderCell>승계신청일</CTableHeaderCell>
        <CTableHeaderCell>매매계약일</CTableHeaderCell>
        <CTableHeaderCell>변경인가일</CTableHeaderCell>
        <CTableHeaderCell>변경인가여부</CTableHeaderCell>
        <CTableHeaderCell>확인</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody>
      <CTableRow
        v-for="suc in successionList"
        :key="suc.pk"
        :class="suc.is_approval ? 'bg-light' : ''"
      >
        <Succession :succession="suc" @on-submit="onSubmit" />
      </CTableRow>
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="successionPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
