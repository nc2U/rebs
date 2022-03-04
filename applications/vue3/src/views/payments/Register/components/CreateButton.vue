<template>
  <CAlert color="secondary" class="text-right">
    <CButton
      type="button"
      color="primary"
      @click="showDetail"
      :disabled="!contract"
    >
      신규납부 등록
    </CButton>
  </CAlert>

  <FormModal size="lg" ref="createFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      건별 수납 관리 [신규 납부등록]
    </template>
    <template v-slot:default>
      <PaymentForm
        @on-submit="createConfirm"
        @on-delete="deleteConfirm"
        @close="$refs.createFormModal.visible = false"
      />
    </template>
  </FormModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import PaymentForm from '@/views/payments/Register/components/PaymentForm.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'CreateButton',
  components: { FormModal, PaymentForm },
  props: { contract: Object },
  computed: {
    pageManageAuth() {
      return (
        this.superAuth || (this.staffAuth && this.staffAuth.payment === '2')
      )
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    showDetail(this: any) {
      this.$refs.createFormModal.callModal()
    },
    createConfirm(this: any, payload: any) {
      if (this.pageManageAuth) this.createObject(payload)
      else this.$refs.alertModal.callModal()
    },
    createObject(this: any, payload: any) {
      this.$emit('on-create', payload)
      this.$refs.createFormModal.visible = false
    },
  },
})
</script>
