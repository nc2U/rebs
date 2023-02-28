<script lang="ts" setup>
import { computed } from 'vue'
import { useProject } from '@/store/pinia/project'
import { ProOutBudget } from '@/store/types/project'
import { TableSecondary } from '@/utils/cssMixins'
import OutBudget from './OutBudget.vue'

const emit = defineEmits(['on-update', 'on-delete'])

const proStore = useProject()
const proOutBudgetList = computed(() => proStore.proOutBudgetList)

const onUpdateOrder = (payload: ProOutBudget) => emit('on-update', payload)
const onDeleteOrder = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col width="13%" />
      <col width="13%" />
      <col width="20%" />
      <col width="25%" />
      <col width="16%" />
      <col width="13%" />
    </colgroup>
    <CTableHead :color="TableSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>대분류</CTableHeaderCell>
        <CTableHeaderCell>중분류</CTableHeaderCell>
        <CTableHeaderCell>예산항목명칭</CTableHeaderCell>
        <CTableHeaderCell>산출근거</CTableHeaderCell>
        <CTableHeaderCell>수입예산</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="proOutBudgetList.length > 0">
      <OutBudget
        v-for="budget in proOutBudgetList"
        :key="budget.pk"
        :budget="budget"
        @on-update="onUpdateOrder"
        @on-delete="onDeleteOrder"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell colspan="6" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
