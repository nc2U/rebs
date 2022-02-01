<template>
  <CTable hover responsive>
    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell>등록차수</CTableHeaderCell>
        <CTableHeaderCell>차수구분</CTableHeaderCell>
        <CTableHeaderCell>차수그룹명칭</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="projectOrderGroup">
      <CTableRow
        v-for="order in projectOrderGroup"
        :key="order.id"
        class="text-center"
      >
        <CTableDataCell>{{ order.order_number }}</CTableDataCell>
        <CTableDataCell>{{ order.sort_desc }}</CTableDataCell>
        <CTableDataCell>{{ order.order_group_name }}</CTableDataCell>
        <CTableDataCell>
          <CButton color="success" size="sm">수정</CButton>
          <CButton color="danger" size="sm">삭제</CButton>
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell>등록된 데이터가 없습니다.</CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapActions, mapGetters, mapState } from 'vuex'
import project from '@/store/modules/project'

export default defineComponent({
  name: 'OrderForm',
  props: ['project'],
  created() {
    this.fetchOrderGroupList()
  },
  computed: {
    projectOrderGroup() {
      return this.project ? this.OrderGroupByProject(this.project.id) : null
    },
    ...mapState('contract', ['orderGroupList']),
    ...mapGetters('contract', ['OrderGroupByProject']),
  },
  methods: {
    ...mapActions('contract', ['fetchOrderGroupList']),
  },
})
</script>

<style lang="scss" scoped></style>
