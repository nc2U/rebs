<template>
  <CAlert color="secondary">
    <CButton color="primary" @click="createConfirm">등록하기</CButton>
  </CAlert>

  <FormModal size="lg" ref="cancelFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      계약 해지 등록
    </template>
    <template v-slot:default>
      <ContCancelForm
        @on-submit="onSubmit"
        @close="$refs.cancelFormModal.visible = false"
      />
    </template>
  </FormModal>

  <AlertModal ref="cancelAlertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import ContCancelForm from '@/views/contracts/Cancel/components/ContCancelForm.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'AddCancelCont',
  components: { FormModal, ContCancelForm },
  computed: {
    pageManageAuth(this: any) {
      return (
        this.superAuth || (this.staffAuth && this.staffAuth.contract === '2')
      )
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    createConfirm(this: any) {
      if (this.pageManageAuth) this.$refs.cancelFormModal.callModal()
      else this.$refs.cancelAlertModal.callModal()
    },
    onSubmit(this: any, payload: any) {
      this.$emit('on-submit', payload)
      this.$refs.cancelFormModal.visible = false
    },
  },
})
</script>
