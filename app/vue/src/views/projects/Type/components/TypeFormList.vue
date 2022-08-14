<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Type from '@/views/projects/Type/components/Type.vue'
import { headerSecondary } from '@/utils/cssMixins'

const emit = defineEmits(['on-update', 'on-delete'])

const store = useStore()
const unitTypeList = computed(() => store.state.project.unitTypeList)

const onUpdateType = (payload: any) => {
  emit('on-update', payload)
}
const onDeleteType = (pk: number) => {
  emit('on-delete', pk)
}
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col width="13%" />
      <col width="10%" />
      <col width="13%" />
      <col width="13%" />
      <col width="13%" />
      <col width="13%" />
      <col width="13%" />
      <col width="12%" />
    </colgroup>
    <CTableHead :color="headerSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>타입명칭</CTableHeaderCell>
        <CTableHeaderCell>타입색상</CTableHeaderCell>
        <CTableHeaderCell>전용면적(m<sup>2</sup>)</CTableHeaderCell>
        <CTableHeaderCell>공급면적(m<sup>2</sup>)</CTableHeaderCell>
        <CTableHeaderCell>계약면적(m<sup>2</sup>)</CTableHeaderCell>
        <CTableHeaderCell>평균가격</CTableHeaderCell>
        <CTableHeaderCell>세대수</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="unitTypeList.length > 0">
      <Type
        v-for="type in unitTypeList"
        :key="type.pk"
        :type="type"
        @on-update="onUpdateType"
        @on-delete="onDeleteType"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell colspan="8" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
