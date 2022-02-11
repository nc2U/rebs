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
          v-model.number="form.order_number"
          placeholder="등록차수"
          type="number"
          min="1"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormSelect v-model="form.sort" :disabled="!selected" required>
          <option value="">구분선택</option>
          <option value="1">일반분양</option>
          <option value="2">조합모집</option>
        </CFormSelect>
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.order_group_name"
          placeholder="차수그룹 명칭"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" :disabled="!selected">그룹추가</CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-info" />
      차수그룹 등록
    </template>
    <template v-slot:default>
      프로젝트의 차수그룹 정보 등록을 진행하시겠습니까?
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
  name: 'OrderAddForm',
  components: { ConfirmModal },
  data() {
    return {
      form: {
        order_number: null,
        sort: '',
        order_group_name: '',
      },
      validated: false,
    }
  },
  props: ['selected'],
  methods: {
    onSubmit(event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        this.validated = true
      } else {
        ;(this as any).$refs.confirmModal.callModal()
      }
    },
    modalAction() {
      this.$emit('on-submit', this.form)
      this.validated = false
      ;(this as any).$refs.confirmModal.visible = false
      this.resetForm()
    },
    resetForm() {
      this.form.order_number = null
      this.form.sort = ''
      this.form.order_group_name = ''
    },
  },
})
</script>
