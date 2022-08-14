<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import OrderGroup from './OrderGroup.vue'
import { headerSecondary } from '@/utils/cssMixins'

const emit = defineEmits(['on-update', 'on-delete'])

const store = useStore()
const orderGroupList = computed(() => store.state.contract.orderGroupList)

const onUpdateOrder = (payload: any) => emit('on-update', payload)
const onDeleteOrder = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col width="25%" />
      <col width="25%" />
      <col width="25%" />
      <col width="25%" />
    </colgroup>
    <CTableHead :color="headerSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>등록차수</CTableHeaderCell>
        <CTableHeaderCell>차수구분</CTableHeaderCell>
        <CTableHeaderCell>차수그룹명</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="orderGroupList.length > 0">
      <OrderGroup
        v-for="order in orderGroupList"
        :key="order.pk"
        :order="order"
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
