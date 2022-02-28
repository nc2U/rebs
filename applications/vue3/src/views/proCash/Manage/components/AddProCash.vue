<template>
  <CAlert color="secondary" class="text-right">
    <CButton color="primary" @click="createConfirm">신규등록</CButton>
  </CAlert>

  <FormModal size="lg" ref="createFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      프로젝트 입출금 거래 건별 등록
    </template>
    <template v-slot:default>
      <CreateForm
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
import CreateForm from '@/views/proCash/Manage/components/CreateForm.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'AddProCash',
  components: { FormModal, CreateForm },
  computed: {
    pageManageAuth() {
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
    createObject(this: any, payload: any) {
      this.$emit('on-create', payload)
      this.$refs.createFormModal.visible = false
    },
  },
})
</script>
