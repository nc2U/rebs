<script lang="ts" setup="">
import { computed } from 'vue'
import { useCompany } from '@/store/pinia/company'
import { headerSecondary } from '@/utils/cssMixins'
import Pagination from '@/components/Pagination'
import Rank from './Rank.vue'

const emit = defineEmits(['page-select'])

const companyStore = useCompany()
const rankList = computed(() => companyStore.rankList)
const ranksCount = computed(() => companyStore.ranksCount)

const rankPages = (page: number) => companyStore.rankPages(page)
const pageSelect = (page: number) => emit('page-select', page)

const showDetail = () => alert('준비중!!')
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="7%" />
      <col width="10%" />
      <col width="13%" />
      <col width="25%" />
      <col width="38%" />
      <col width="7%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell scope="col">No</CTableHeaderCell>
        <CTableHeaderCell scope="col">구분</CTableHeaderCell>
        <CTableHeaderCell scope="col">직급</CTableHeaderCell>
        <CTableHeaderCell scope="col">직함</CTableHeaderCell>
        <CTableHeaderCell scope="col">설명</CTableHeaderCell>
        <CTableHeaderCell scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Rank
        v-for="rank in rankList"
        :key="rank.pk"
        :rank="rank"
        @show-detail="showDetail"
      />
    </CTableBody>
  </CTable>

  <Pagination
    v-if="ranksCount > 10"
    :active-page="1"
    :limit="8"
    :pages="rankPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
