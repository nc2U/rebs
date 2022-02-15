<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2" color="success">
      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.name"
          placeholder="동(건물) 이름"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="3" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" :disabled="disabled">호 추가</CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-info" />
      호(건물) 등록
    </template>
    <template v-slot:default>
      프로젝트의 호(건물) 정보 등록을 진행하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

export default defineComponent({
  name: 'UnitAddForm',
  components: { ConfirmModal },
  data() {
    return {
      form: {
        name: '',
      },
      validated: false,
    }
  },
  props: ['disabled'],
  methods: {
    onSubmit(this: any, event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        this.validated = true
      } else {
        this.$refs.confirmModal.callModal()
      }
    },
    modalAction() {
      this.$emit('on-submit', this.form)
      this.validated = false
      ;(this as any).$refs.confirmModal.visible = false
      this.resetForm()
    },
    resetForm() {
      this.form.name = ''
    },
  },
})
</script>
