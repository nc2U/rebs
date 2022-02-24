<template>
  <CTableRow class="text-center">
    <CTableDataCell>2020-01-01</CTableDataCell>
    <CTableDataCell>출금</CTableDataCell>
    <CTableDataCell>금융비</CTableDataCell>
    <CTableDataCell>브리지 이자</CTableDataCell>
    <CTableDataCell>담보대출 이자</CTableDataCell>
    <CTableDataCell>동춘1구역9블럭..</CTableDataCell>
    <CTableDataCell>무궁화-이자1(새마을)</CTableDataCell>
    <CTableDataCell>-</CTableDataCell>
    <CTableDataCell>261,736,850</CTableDataCell>
    <CTableDataCell>증빙없음</CTableDataCell>
    <CTableDataCell>
      <CButton color="success" @click="updatePayment" size="sm"> 수정</CButton>
      <CButton color="danger" @click="deletePayment" size="sm"> 삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      입출금 거래 건별 수정
    </template>
    <template v-slot:default>
      해당 입출금거래 정보 수정 등록을 진행하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ProCash',
  mixins: [commonMixin],
  components: { ConfirmModal, AlertModal },
  props: {
    payment: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    updatePayment(this: any) {
      if (this.superAuth || (this.staffAuth && this.staffAuth.payment === '2'))
        this.$emit('on-update', { ...{ pk: this.payment.pk }, ...this.form })
      else this.$refs.alertModal.callModal()
    },
    deletePayment(this: any) {
      if (this.superAuth || (this.staffAuth && this.staffAuth.payment === '2'))
        this.$emit('on-delete', this.payment.pk)
      else this.$refs.alertModal.callModal()
    },
  },
})
</script>
