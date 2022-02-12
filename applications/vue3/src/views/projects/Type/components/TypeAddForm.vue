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
          placeholder="타입명칭"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="1" class="mb-2">
        <CFormInput
          v-model="form.color"
          title="타입색상"
          type="color"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model.number="form.average_price"
          placeholder="평균가격"
          type="number"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model.number="form.num_unit"
          placeholder="세대수"
          type="number"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="2" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" :disabled="disabled">타입추가</CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-info" />
      타입 정보 등록
    </template>
    <template v-slot:default>
      프로젝트의 타입 정보 등록을 진행하시겠습니까?
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
  name: 'TypeAddForm',
  components: { ConfirmModal },
  data() {
    return {
      form: {
        name: '',
        color: '',
        average_price: null,
        num_unit: null,
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
    modalAction(this: any) {
      this.$emit('on-submit', this.form)
      this.validated = false
      this.$refs.confirmModal.visible = false
      this.resetForm()
    },
    resetForm() {
      this.form.name = ''
      this.form.color = ''
      this.form.average_price = null
      this.form.num_unit = null
    },
  },
})
</script>
