<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        type="number"
        v-model="form.order_number"
        min="1"
        required
        placeholder="등록차수"
        @keypress.enter="onUpdateOrder"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect
        v-model="form.sort"
        :options="sorts"
        :selected="sorts.value == form.sort"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.order_group_name"
        @keypress.enter="onUpdateOrder"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton color="success" size="sm" @click="onUpdateOrder"> 수정</CButton>
      <CButton color="danger" size="sm" @click="onDeleteOrder">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-warning" />
      삭제 확인!
    </template>
    <template v-slot:default>
      이 그룹에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후 삭제가능
      합니다. 해당 차수그룹을 삭제 하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

export default defineComponent({
  name: 'OrderGroup',
  components: { ConfirmModal },
  data() {
    return {
      sorts: [
        { label: '일반분양', value: '1' },
        { label: '조합모집', value: '2' },
      ],
      form: {
        order_number: null,
        sort: '',
        order_group_name: '',
      },
      validated: false,
    }
  },
  props: {
    order: {
      type: Object,
    },
  },
  created() {
    if (this.order) {
      this.form.order_number = this.order.order_number
      this.form.sort = this.order.sort
      this.form.order_group_name = this.order.order_group_name
    }
  },
  watch: {
    order(this: any) {
      this.form.order_number = this.order.order_number
      this.form.sort = this.order.sort
      this.form.order_group_name = this.order.order_group_name
    },
  },
  methods: {
    onUpdateOrder(this: any) {
      const pk = this.order.pk
      this.$emit('on-update', { ...{ pk }, ...this.form })
    },
    onDeleteOrder(this: any) {
      this.$refs.confirmModal.callModal()
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.order.pk)
      this.$refs.confirmModal.visible = false
    },
  },
})
</script>
