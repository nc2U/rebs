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
          v-model="form.order_number"
          placeholder="등록차수"
          type="number"
          min="1"
          required
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormSelect v-model="form.sort" required>
          <option v-for="(sort, i) in sorts" :value="sort.value" :key="i">
            {{ sort.label }}
          </option>
        </CFormSelect>
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.order_group_name"
          placeholder="차수그룹 명칭"
          required
        />
      </CCol>

      <CCol md="3" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary">그룹추가</CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>&lt;진행 확인!&gt;</template>
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
      sorts: [
        { label: '구분선택', value: '' },
        { label: '일반분양', value: '1' },
        { label: '조합모집', value: '2' },
      ],
      form: {
        order_number: null,
        sort: '',
        order_group_name: '',
      },
      validated: false,
    }
  },
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
    },
  },
})
</script>
