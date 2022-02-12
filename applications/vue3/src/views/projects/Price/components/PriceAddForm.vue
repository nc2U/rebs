<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2" color="success">
      <CCol md="2" class="mb-2" color="success">
        <CFormInput
          v-model.number="form.price_build"
          type="number"
          min="0"
          placeholder="타입별 건물가"
          :disabled="!selected || !addActive"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model.number="form.price_land"
          type="number"
          min="0"
          placeholder="타입별 대지가"
          :disabled="!selected || !addActive"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model.number="form.price_tax"
          type="number"
          min="0"
          placeholder="타입별 부가세"
          :disabled="!selected || !addActive"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model.number="form.price"
          type="number"
          min="0"
          required
          placeholder="타입별 공급가격"
          :disabled="!selected || !addActive"
        />
      </CCol>

      <CCol md="2" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" :disabled="!selected || !addActive">
          공급가추가
        </CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-info" />
      공급가격 정보 등록
    </template>
    <template v-slot:default>
      프로젝트의 공급가격 정보 등록을 진행하시겠습니까?
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
  name: 'PriceAddForm',
  components: { ConfirmModal },
  data() {
    return {
      form: {
        price_build: null,
        price_land: null,
        price_tax: null,
        price: null,
      },
      price: {},
      validated: false,
    }
  },
  props: ['selected', 'addActive'],
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
      this.form.price_build = null
      this.form.price_land = null
      this.form.price_tax = null
      this.form.price = null
    },
  },
})
</script>
