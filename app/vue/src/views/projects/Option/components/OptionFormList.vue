<script lang="ts" setup>
import { computed } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import { type UnitType } from '@/store/types/project'
import { TableSecondary } from '@/utils/cssMixins'
import Option from '@/views/projects/Option/components/Option.vue'

const emit = defineEmits(['on-update', 'on-delete'])

const projectDataStore = useProjectData()
const unitTypeList = computed(() => projectDataStore.unitTypeList)

const onUpdateType = (payload: UnitType) => emit('on-update', payload)
const onDeleteType = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col style="width: 13%" />
      <col style="width: 13%" />
      <col style="width: 13%" />
      <col style="width: 13%" />
      <col style="width: 38%" />
      <col style="width: 10%" />
    </colgroup>
    <CTableHead :color="TableSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>타입</CTableHeaderCell>
        <CTableHeaderCell>옵션 코드</CTableHeaderCell>
        <CTableHeaderCell>옵션 명칭</CTableHeaderCell>
        <CTableHeaderCell>옵션 가격</CTableHeaderCell>
        <CTableHeaderCell>상세 설명</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="unitTypeList.length > 0">
      <Option
        v-for="type in unitTypeList"
        :key="type.pk"
        :type="type"
        @on-update="onUpdateType"
        @on-delete="onDeleteType"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell colspan="9" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
