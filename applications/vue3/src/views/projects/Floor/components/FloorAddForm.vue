<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2">
      <CCol md="2" class="mb-2">
        <CFormInput
          v-model.number="form.start_floor"
          placeholder="시작 층"
          type="number"
          min="0"
          required
          :disabled="!disabled"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model.number="form.end_floor"
          placeholder="종료 층"
          type="number"
          min="0"
          required
          :disabled="!disabled"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model="form.extra_cond"
          placeholder="방향/위치(옵션)"
          :disabled="!disabled"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model="form.alias_name"
          placeholder="층별 범위 명칭"
          required
          :disabled="!disabled"
        />
      </CCol>

      <CCol md="2" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" :disabled="!disabled">층별타입추가</CButton>
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
        start_floor: '',
        end_floor: '',
        extra_cond: '',
        alias_name: '',
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
      this.form.start_floor = ''
      this.form.end_floor = ''
      this.form.extra_cond = ''
      this.form.alias_name = ''
    },
  },
})
</script>
