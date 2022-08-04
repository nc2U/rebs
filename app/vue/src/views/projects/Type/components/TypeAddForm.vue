<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2">
      <CCol lg="6">
        <CRow>
          <CCol lg="4" class="mb-2">
            <CFormInput
              v-model="form.name"
              placeholder="타입명칭"
              required
              :disabled="disabled"
            />
          </CCol>

          <CCol lg="2" class="mb-2">
            <CFormInput
              v-model="form.color"
              title="타입색상"
              type="color"
              required
              :disabled="disabled"
            />
          </CCol>

          <CCol lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.actual_area"
              placeholder="전용면적"
              type="number"
              min="0"
              step="0.0001"
              :disabled="disabled"
            />
            <CFormFeedback invalid>
              전용면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>

          <CCol lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.supply_area"
              placeholder="공급면적"
              type="number"
              min="0"
              step="0.0001"
              :disabled="disabled"
            />
            <CFormFeedback invalid>
              공급면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>
      </CCol>
      <CCol lg="6">
        <CRow>
          <CCol lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.contract_area"
              placeholder="계약면적"
              type="number"
              min="0"
              step="0.0001"
              :disabled="disabled"
            />
            <CFormFeedback invalid>
              계약면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>

          <CCol lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.average_price"
              placeholder="평균가격"
              type="number"
              min="0"
              required
              :disabled="disabled"
            />
          </CCol>

          <CCol lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.num_unit"
              placeholder="세대수"
              type="number"
              required
              :disabled="disabled"
            />
          </CCol>

          <CCol lg="3" class="d-grid gap-2 d-lg-block mb-3">
            <CButton color="primary" :disabled="disabled">타입추가</CButton>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-info" />
      타입 정보 등록
    </template>
    <template #default>
      프로젝트의 타입 정보 등록을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'TypeAddForm',
  components: { ConfirmModal, AlertModal },
  props: { disabled: Boolean },
  data() {
    return {
      form: {
        name: '',
        color: '',
        actual_area: null,
        supply_area: null,
        contract_area: null,
        average_price: null,
        num_unit: null,
      },
      validated: false,
    }
  },
  computed: {
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    onSubmit(this: any, event: any) {
      if (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.project === '2')
      ) {
        const form = event.currentTarget
        if (form.checkValidity() === false) {
          event.preventDefault()
          event.stopPropagation()

          this.validated = true
        } else {
          this.$refs.confirmModal.callModal()
        }
      } else {
        this.$refs.alertModal.callModal()
        this.resetForm()
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
      this.form.actual_area = null
      this.form.supply_area = null
      this.form.contract_area = null
      this.form.average_price = null
      this.form.num_unit = null
    },
  },
})
</script>
