<template>
  <CAlert color="secondary" class="text-right">
    <CButton color="primary" @click="createConfirm">신규등록</CButton>
  </CAlert>

  <FormModal size="lg" ref="createFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      운영비(전도금) 거래 건별 등록
    </template>
    <template v-slot:default>
      <ProImprestForm
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
import ProImprestForm from '@/views/proCash/Imprest/components/ProImprestForm.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'AddProImprest',
  components: { FormModal, ProImprestForm },
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
