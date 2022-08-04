<template>
  <CAlert color="secondary" class="text-right">
    <CButton color="primary" @click="createConfirm">신규등록</CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      입출금 거래 건별 등록
    </template>
    <template #default>
      <CashForm
        @on-submit="createObject"
        @close="$refs.createFormModal.visible = false"
      />
    </template>
  </FormModal>

  <AlertModal ref="createAlertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import CashForm from '@/views/comCash/Manage/components/CashForm.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'AddCash',
  components: { FormModal, CashForm },
  computed: {
    pageManageAuth() {
      return (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.company_cash === '2')
      )
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    createConfirm(this: any) {
      if (this.pageManageAuth) this.$refs.createFormModal.callModal()
      else this.$refs.createAlertModal.callModal()
    },
    createObject(this: any, payload: any) {
      this.$emit('on-create', payload)
      this.$refs.createFormModal.visible = false
    },
  },
})
</script>
