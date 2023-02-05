<script lang="ts" setup>
import { computed } from 'vue'
import { useSite } from '@/store/pinia/project_site'
import { SiteContract as siteCont } from '@/store/types/project'
import { TableSecondary } from '@/utils/cssMixins'
import SiteContract from './SiteContract.vue'
import Pagination from '@/components/Pagination'

const emit = defineEmits(['page-select', 'on-delete', 'multi-submit'])

const siteStore = useSite()
const siteContList = computed(() => siteStore.siteContList)
const siteContCount = computed(() => siteStore.siteContCount)

const siteContPages = (num: number) => Math.ceil(siteContCount.value / num)
const pageSelect = (page: number) => emit('page-select', page)
const multiSubmit = (payload: siteCont) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="5%" />
      <col width="9%" />
      <col width="9%" />
      <col width="7%" />
      <col width="7%" />
      <col width="10%" />
      <col width="9%" />
      <col width="5%" />
      <col width="9%" />
      <col width="9%" />
      <col width="10%" />
      <col width="5%" />
      <col width="6%" />
    </colgroup>

    <CTableHead :color="TableSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell rowspan="2" scope="col">
          소유<br />구분
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">소유자</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">계약일</CTableHeaderCell>
        <CTableHeaderCell colspan="2" scope="col">
          총계약 면적
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">
          총매매<br />대금
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">계약금1</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">
          지급<br />여부
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">계약금2</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">중도금</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">잔금</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">
          지급<br />여부
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">비고</CTableHeaderCell>
      </CTableRow>
      <CTableRow class="text-center">
        <CTableHeaderCell scope="col">m<sup>2</sup></CTableHeaderCell>
        <CTableHeaderCell scope="col">평</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <SiteContract
        v-for="cont in siteContList"
        :key="cont.pk"
        :contract="cont"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    v-if="siteContCount > 10"
    :active-page="1"
    :limit="8"
    :pages="siteContPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
