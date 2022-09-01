<script lang="ts" setup>
import { computed } from 'vue'
import { useSite } from '@/store/pinia/project_site'
import { headerSecondary } from '@/utils/cssMixins'
import SiteContract from './SiteContract.vue'
import Pagination from '@/components/Pagination'

const emit = defineEmits(['page-select', 'on-delete', 'multi-submit'])

const siteStore = useSite()
const siteList = computed(() => siteStore.getSiteList)
const siteCount = computed(() => siteStore.siteCount)

const sitePages = (num: number) => Math.ceil(siteCount.value / num)
const pageSelect = (page: number) => emit('page-select', page)
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="6%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="6%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell rowspan="2" scope="col">No</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">소유자</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">계약일</CTableHeaderCell>
        <CTableHeaderCell colspan="2" scope="col">총계약 면적</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">총매매 대금</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">계약금1</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">지급여부</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">계약금2</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">중도금1</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">중도금2</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">잔금</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">지급여부</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">비고</CTableHeaderCell>
      </CTableRow>
      <CTableRow class="text-center">
        <CTableHeaderCell scope="col">m<sup>2</sup></CTableHeaderCell>
        <CTableHeaderCell scope="col">평</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <SiteContract
        v-for="site in siteList"
        :key="site.pk"
        :site="site"
        :is-returned="isReturned"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    v-if="siteCount > 10"
    :active-page="1"
    :limit="8"
    :pages="sitePages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
