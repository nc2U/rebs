<template>
  <CAlert color="secondary" class="text-right">
    <CButton
      type="button"
      color="primary"
      :disabled="btnActive"
      @click="showDetail"
    >
      신규납부 등록
    </CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      건별 수납 관리 [신규 납부등록]
    </template>
    <template #default>
      <PaymentForm
        :contract="contract"
        @on-submit="createObject"
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
    btnActive() {
      return !this.contract
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    showDetail(this: any) {
      this.$refs.createFormModal.callModal()
    },
    createObject(this: any, payload: any) {
      this.$emit('on-create', payload)
      this.$refs.createFormModal.visible = false
    },
  },
})
</script>
