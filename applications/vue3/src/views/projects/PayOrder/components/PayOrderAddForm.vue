<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2">
      <CCol md="3" class="mb-2">
        <CFormSelect />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model.number="form.pay_code"
          placeholder="납입회차 코드"
          type="number"
          min="0"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model.number="form.pay_time"
          placeholder="납부순서"
          type="number"
          min="0"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.pay_name"
          placeholder="납부회차 명"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.alias_name"
          placeholder="별칭 이름"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.alias_name"
          placeholder="PM용역비 여부"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.pay_due_date"
          placeholder="납부기한일"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.extra_due_date"
          placeholder="납부유예일"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="2" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" :disabled="!selected">층별타입추가</CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-info" />
      층별 타입 등록
    </template>
    <template v-slot:default>
      프로젝트의 층별 범위 타입 정보 등록을 진행하시겠습니까?
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
  name: 'FloorAddForm',
  components: { ConfirmModal },
  data() {
    return {
      form: {
        pay_sort: '',
        pay_code: '',
        pay_time: '',
        pay_name: '',
        alias_name: '',
        is_pm_cost: '',
        pay_due_date: '',
        extra_due_date: '',
      },
      validated: false,
    }
  },
  props: ['selected'],
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
      this.form.pay_sort = ''
      this.form.pay_code = ''
      this.form.pay_time = ''
      this.form.pay_name = ''
      this.form.alias_name = ''
      this.form.is_pm_cost = ''
      this.form.pay_due_date = ''
      this.form.extra_due_date = ''
    },
  },
})
</script>
