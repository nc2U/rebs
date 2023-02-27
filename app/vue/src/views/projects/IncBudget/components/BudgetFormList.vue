<script lang="ts" setup>
import { computed } from 'vue'
import { useProject } from '@/store/pinia/project'
import { TableSecondary } from '@/utils/cssMixins'
import IncBudget from './IncBudget.vue'

const emit = defineEmits(['on-update', 'on-delete'])

const proStore = useProject()
const proIncBudgetList = computed(() => proStore.proIncBudgetList)

const onUpdateOrder = (payload: og) => emit('on-update', payload)
const onDeleteOrder = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="12%" />
    </colgroup>
    <CTableHead :color="TableSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>대분류</CTableHeaderCell>
        <CTableHeaderCell>중분류</CTableHeaderCell>
        <CTableHeaderCell>차수그룹명</CTableHeaderCell>
        <CTableHeaderCell>타입명</CTableHeaderCell>
        <CTableHeaderCell>항목명</CTableHeaderCell>
        <CTableHeaderCell>평균가격</CTableHeaderCell>
        <CTableHeaderCell>수량</CTableHeaderCell>
        <CTableHeaderCell>수입예산</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="proIncBudgetList.length > 0">
      <IncBudget
        v-for="budget in proIncBudgetList"
        :key="budget.pk"
        :budget="budget"
        @on-update="onUpdateOrder"
        @on-delete="onDeleteOrder"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell colspan="4" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
