<template>
  <CAlert color="secondary" class="text-right">
    <CButton color="primary" @click="createConfirm">신규등록</CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      프로젝트 입출금 거래 건별 등록
    </template>
    <template #default>
      <ProCashForm
        @multi-submit="multiSubmit"
        @close="$refs.createFormModal.visible = false"
      />
    </template>
  </FormModal>

  <AlertModal ref="createAlertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import ProCashForm from '@/views/proCash/Manage/components/ProCashForm.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'AddProCash',
  components: { FormModal, ProCashForm },
  computed: {
    pageManageAuth(this: any) {
      return (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.project_cash === '2')
      )
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    createConfirm(this: any) {
      if (this.pageManageAuth) this.$refs.createFormModal.callModal()
      else this.$refs.createAlertModal.callModal()
    },
    multiSubmit(payload: any) {
      this.$emit('multi-submit', payload)
    },
  },
})
</script>
