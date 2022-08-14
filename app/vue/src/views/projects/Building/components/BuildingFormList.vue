<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Building from '@/views/projects/Building/components/Building.vue'
import { headerSecondary } from '@/utils/cssMixins'

const emit = defineEmits(['on-update', 'on-delete'])

const store = useStore()
const buildingList = computed(() => store.state.project.buildingList)

const onUpdateBuilding = (payload: any) => emit('on-update', payload)

const onDeleteBuilding = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col width="50%" />
      <col width="50%" />
    </colgroup>
    <CTableHead :color="headerSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>동(건물)이름</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="buildingList.length > 0">
      <Building
        v-for="building in buildingList"
        :key="building.pk"
        :building="building"
        @on-update="onUpdateBuilding"
        @on-delete="onDeleteBuilding"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell colspan="2" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
