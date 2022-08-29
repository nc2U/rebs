<script lang="ts" setup>
import { computed } from 'vue'
import { useSite } from '@/store/pinia/project_site'
import { headerInfo, headerSuccess, headerSecondary } from '@/utils/cssMixins'
import SiteOwner from '@/views/projects/SiteOwner/components/SiteOwner.vue'
import Pagination from '@/components/Pagination'

defineProps({ isReturned: { type: Boolean } })
const emit = defineEmits(['page-select', 'on-delete', 'multi-submit'])

const siteStore = useSite()
const siteOwnerList = computed(() => siteStore.siteOwnerList)
const siteOwnerCount = computed(() => siteStore.siteOwnerCount)

const ownerPages = (num: number) => Math.ceil(siteOwnerCount.value / num)
const pageSelect = (page: number) => emit('page-select', page)
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="7%" />
      <col width="9%" />
      <col width="11%" />
      <col width="13%" />
      <col width="10%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="6%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center">
        <CTableHeaderCell colspan="5" :color="headerInfo">
          소유자 관련 정보
        </CTableHeaderCell>
        <CTableHeaderCell colspan="5" :color="headerSuccess">
          소유권 관련 정보
        </CTableHeaderCell>
      </CTableRow>
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell rowspan="2" scope="col">소유구분</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">소유자</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">생년월일</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">주연락처</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">
          소유부지(지번)
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">소유지분(%)</CTableHeaderCell>
        <CTableHeaderCell colspan="2" scope="col">
          소유면적 <span v-if="isReturned">(환지면적 기준)</span>
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">
          소유권 취득일
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">비고</CTableHeaderCell>
      </CTableRow>
      <CTableRow class="text-center">
        <CTableHeaderCell scope="col">m<sup>2</sup></CTableHeaderCell>
        <CTableHeaderCell scope="col">평</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <SiteOwner
        v-for="owner in siteOwnerList"
        :key="owner.pk"
        :owner="owner"
        :is-returned="isReturned"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="ownerPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
