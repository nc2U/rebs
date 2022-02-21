<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.order_number"
        type="number"
        min="1"
        required
        placeholder="등록차수"
        @keypress.enter="formCheck(form.order_number !== order.order_number)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.sort">
        <option value="">구분선택</option>
        <option value="1">일반분양</option>
        <option value="2">조합모집</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.order_group_name"
        placeholder="차수그룹명"
        @keypress.enter="
          formCheck(form.order_group_name !== order.order_group_name)
        "
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        @click="onUpdateOrder"
        :disabled="formsCheck"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteOrder">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-warning" />
      차수그룹 삭제
    </template>
    <template v-slot:default>
      이 그룹에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후 삭제가능
      합니다. 해당 차수그룹을 삭제 하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'OrderGroup',
  components: { ConfirmModal, AlertModal },
  data() {
    return {
      form: {
        order_number: null,
        sort: '',
        order_group_name: '',
      },
      validated: false,
    }
  },
  props: ['order'],
  created() {
    if (this.order) this.resetForm()
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.order_number === this.order.order_number
      const b = this.form.sort === this.order.sort
      const c = this.form.order_group_name === this.order.order_group_name
      return a && b && c
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    formCheck(bool: boolean) {
      if (bool) this.onUpdateOrder()
      return
    },
    onUpdateOrder(this: any) {
      if (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.project === '2')
      ) {
        const pk = this.order.pk
        this.$emit('on-update', { ...{ pk }, ...this.form })
      } else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    onDeleteOrder(this: any) {
      if (this.superAuth || (this.staffAuth && this.staffAuth.project === '2'))
        this.$refs.confirmModal.callModal()
      else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.order.pk)
      this.$refs.confirmModal.visible = false
    },
    resetForm() {
      this.form.order_number = this.order.order_number
      this.form.sort = this.order.sort
      this.form.order_group_name = this.order.order_group_name
    },
  },
})
</script>
