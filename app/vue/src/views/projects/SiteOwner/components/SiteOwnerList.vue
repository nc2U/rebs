<script lang="ts" setup>
import { computed } from 'vue'
import { useSite } from '@/store/pinia/project_site'
import { headerSecondary } from '@/utils/cssMixins'
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
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="6%" />
      <col width="7%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col v-if="isReturned" width="8%" />
      <col v-if="isReturned" width="8%" />
      <col width="33%" />
      <col width="6%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center">
        <CTableHeaderCell rowspan="2" scope="col">No</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">행정동</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">지번</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">지목</CTableHeaderCell>
        <CTableHeaderCell colspan="2" scope="col">공부상 면적</CTableHeaderCell>
        <CTableHeaderCell v-if="isReturned" colspan="2" scope="col">
          환지 면적
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">소유자 목록</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">비고</CTableHeaderCell>
      </CTableRow>
      <CTableRow class="text-center">
        <CTableHeaderCell scope="col">m<sup>2</sup></CTableHeaderCell>
        <CTableHeaderCell scope="col">평</CTableHeaderCell>
        <CTableHeaderCell v-if="isReturned" scope="col">
          m<sup>2</sup>
        </CTableHeaderCell>
        <CTableHeaderCell v-if="isReturned" scope="col">평</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <SiteOwner
        v-for="owner in siteOwnerList"
        :key="owner.pk"
        :site="owner"
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
