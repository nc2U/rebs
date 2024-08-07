<script lang="ts" setup>
import { computed } from 'vue'
import { useCompany } from '@/store/pinia/company'
import { TableSecondary } from '@/utils/cssMixins'
import { write_human_resource } from '@/utils/pageAuth'
import { type Duty as DutyType } from '@/store/types/company'
import Pagination from '@/components/Pagination'
import Duty from './Duty.vue'

const emit = defineEmits(['page-select', 'multi-submit', 'on-delete'])

const companyStore = useCompany()
const dutyList = computed(() => companyStore.dutyList)
const dutysCount = computed(() => companyStore.dutysCount)

const dutyPages = (page: number) => companyStore.dutyPages(page)
const pageSelect = (page: number) => emit('page-select', page)
const multiSubmit = (payload: DutyType) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col style="width: 7%" />
      <col style="width: 13%" />
      <col style="width: 73%" />
      <col v-if="write_human_resource" style="width: 7%" />
    </colgroup>

    <CTableHead :color="TableSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell scope="col">No</CTableHeaderCell>
        <CTableHeaderCell scope="col">직책명</CTableHeaderCell>
        <CTableHeaderCell scope="col">설명</CTableHeaderCell>
        <CTableHeaderCell v-if="write_human_resource" scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Duty
        v-for="duty in dutyList"
        :key="duty.pk"
        :duty="duty"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    v-if="dutysCount > 10"
    :active-page="1"
    :limit="8"
    :pages="dutyPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
