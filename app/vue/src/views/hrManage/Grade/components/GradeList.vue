<script lang="ts" setup="">
import { computed } from 'vue'
import { useCompany } from '@/store/pinia/company'
import { headerSecondary } from '@/utils/cssMixins'
import { Grade as GradeType } from '@/store/types/company'
import Pagination from '@/components/Pagination'
import Grade from './Grade.vue'

const emit = defineEmits(['page-select', 'multi-submit', 'on-delete'])

const comStore = useCompany()
const gradeList = computed(() => comStore.gradeList)
const gradesCount = computed(() => comStore.gradesCount)

const gradePages = (page: number) => comStore.gradePages(page)
const pageSelect = (page: number) => emit('page-select', page)
const multiSubmit = (payload: GradeType) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="13%" />
      <col width="13%" />
      <col width="38%" />
      <col width="7%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell scope="col">직급명</CTableHeaderCell>
        <CTableHeaderCell scope="col">승급년수</CTableHeaderCell>
        <CTableHeaderCell scope="col">신입부여 기준</CTableHeaderCell>
        <CTableHeaderCell scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Grade
        v-for="grade in gradeList"
        :key="grade.pk"
        :grade="grade"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    v-if="gradesCount > 10"
    :active-page="1"
    :limit="8"
    :pages="gradePages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
