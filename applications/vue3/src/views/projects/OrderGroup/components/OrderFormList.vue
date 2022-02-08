<template>
  <CTable hover responsive>
    <colgroup>
      <col width="25%" />
      <col width="25%" />
      <col width="25%" />
      <col width="25%" />
    </colgroup>
    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell>등록차수</CTableHeaderCell>
        <CTableHeaderCell>차수구분</CTableHeaderCell>
        <CTableHeaderCell>차수그룹명칭</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="project && orderGroupList.length !== 0">
      <OrderGroup
        v-for="order in orderGroupList"
        :key="order.id"
        :order="order"
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

<script lang="ts">
import { defineComponent } from 'vue'
import OrderGroup from './OrderGroup.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'OrderForm',
  components: { OrderGroup },

  props: ['project'],
  computed: {
    ...mapState('contract', ['orderGroupList']),
    // ...mapGetters('contract', ['OrderGroupByProject']),
  },
})
</script>

<style lang="scss" scoped></style>
