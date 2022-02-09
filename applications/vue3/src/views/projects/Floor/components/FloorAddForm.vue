<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2">
      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.start_floor"
          title="시작 층"
          type="number"
          min="0"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.end_floor"
          placeholder="종료 층"
          type="number"
          min="0"
          required
          :disabled="!selected"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.alias_name"
          placeholder="층별 범위 명칭"
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
        start_floor: '',
        end_floor: '',
        alias_name: null,
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
    },
  },
})
</script>
