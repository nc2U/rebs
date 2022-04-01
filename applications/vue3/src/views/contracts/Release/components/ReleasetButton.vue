<template>
  <CAlert color="secondary">
    <CButton
      :color="contractor && contractor.status > '2' ? 'warning' : 'danger'"
      @click="createConfirm"
    >
      {{ contractor && contractor.status > '2' ? '수정하기' : '등록하기' }}
    </CButton>
  </CAlert>

  <FormModal size="lg" ref="releaseFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      계약 해지 신규 등록
    </template>
    <template v-slot:default>
      <ReleaseForm
        :contractor="contractor"
        :release="contRelease"
        @on-submit="onSubmit"
        @close="$refs.releaseFormModal.visible = false"
      />
    </template>
  </FormModal>

  <AlertModal ref="releaseAlertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import ReleaseForm from '@/views/contracts/Release/components/ReleaseForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ReleaseButton',
  components: { FormModal, ReleaseForm, AlertModal },
  props: { contractor: Object, release: Object },
  computed: {
    pageManageAuth(this: any) {
      return (
        this.superAuth || (this.staffAuth && this.staffAuth.contract === '2')
      )
    },
    ...mapState('contract', ['contRelease']),
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    createConfirm(this: any) {
      if (this.pageManageAuth) this.$refs.releaseFormModal.callModal()
      else this.$refs.releaseAlertModal.callModal()
    },
    onSubmit(this: any, payload: any) {
      this.$emit('on-submit', payload)
      this.$refs.releaseFormModal.visible = false
    },
  },
})
</script>
