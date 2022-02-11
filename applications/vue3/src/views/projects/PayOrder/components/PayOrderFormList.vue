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
    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell>종류</CTableHeaderCell>
        <CTableHeaderCell>납입회차 코드</CTableHeaderCell>
        <CTableHeaderCell>납부순서</CTableHeaderCell>
        <CTableHeaderCell>PM용역비 여부</CTableHeaderCell>
        <CTableHeaderCell>납부회차명</CTableHeaderCell>
        <CTableHeaderCell>회차 별칭</CTableHeaderCell>
        <CTableHeaderCell>납부기한일</CTableHeaderCell>
        <CTableHeaderCell>납부유예일</CTableHeaderCell>
        <CTableHeaderCell>비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="selected && payOrderList.length !== 0">
      <PayOrder
        v-for="payOrder in payOrderList"
        @on-update="onUpdatePayOrder"
        @on-delete="onDeletePayOrder"
        :key="payOrder.pk"
        :pay-order="payOrder"
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

<script lang="ts">
import { defineComponent } from 'vue'
import PayOrder from '@/views/projects/PayOrder/components/PayOrder.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'PayOrderFormList',
  components: { PayOrder },
  props: ['project', 'selected'],
  computed: {
    ...mapState('cash', ['payOrderList']),
  },
  methods: {
    onUpdatePayOrder(payload: any) {
      this.$emit('on-update', payload)
    },
    onDeletePayOrder(pk: number) {
      this.$emit('on-delete', pk)
    },
  },
})
</script>
