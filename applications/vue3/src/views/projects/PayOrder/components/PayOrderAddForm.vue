<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2">
      <CCol md="5">
        <CRow>
          <CCol md="3" class="mb-2">
            <CFormSelect v-model="form.pay_sort" :disabled="disabled" required>
              <option value="">종류선택</option>
              <option value="1">계약금</option>
              <option value="2">중도금</option>
              <option value="3">잔 금</option>
            </CFormSelect>
          </CCol>

          <CCol md="3" class="mb-2">
            <CFormInput
              v-model.number="form.pay_code"
              placeholder="납입회차 코드"
              type="number"
              min="0"
              required
              :disabled="disabled"
            />
            <!--        <CFormText>-->
            <!--          프로젝트 내에서 모든 납부회차를 고유 순서대로 숫자로 부여한다.'-->
            <!--        </CFormText>-->
          </CCol>

          <CCol md="3" class="mb-2">
            <CFormInput
              v-model.number="form.pay_time"
              placeholder="납부순서"
              type="number"
              min="0"
              required
              :disabled="disabled"
            />
            <!--        <CFormText-->
            <!--          >동일 납부회차에 2가지 항목을 별도로 납부하여야 하는 경우(ex: 분담금 +-->
            <!--          업무대행료) 하나의 납입회차 코드(ex: 1)에 2개의 납부순서(ex: 1, 2)를-->
            <!--          등록한다.-->
            <!--        </CFormText>-->
          </CCol>
          <CCol md="3" class="mb-2">
            <CRow>
              <CFormLabel class="col-md-8 col-form-label">
                PM용역비 여부
              </CFormLabel>
              <CCol md="1" class="pt-2">
                <CFormSwitch
                  v-model="form.is_pm_cost"
                  :checked="false"
                  :disabled="disabled"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </CCol>

      <CCol md="5">
        <CRow>
          <CCol md="3" class="mb-2">
            <CFormInput
              v-model="form.pay_name"
              placeholder="납부회차 명"
              required
              :disabled="disabled"
            />
          </CCol>
          <CCol md="3" class="mb-2">
            <CFormInput
              v-model="form.alias_name"
              placeholder="별칭 이름"
              :disabled="disabled"
            />
          </CCol>

          <CCol md="3" class="mb-2">
            <CFormInput
              v-model="form.pay_due_date"
              v-maska="'####-##-##'"
              placeholder="납부기한일"
              :disabled="disabled"
            />
          </CCol>

          <CCol md="3" class="mb-2">
            <CFormInput
              v-model="form.extra_due_date"
              v-maska="'####-##-##'"
              placeholder="납부유예일"
              :disabled="disabled"
            />
            <!--        <CFormText>-->
            <!--          연체료 계산 기준은 납부기한일이 원칙이나 이 값이 있는 경우-->
            <!--          납부유예일을 연체료 계산 기준으로 한다.-->
            <!--        </CFormText>-->
          </CCol>
        </CRow>
      </CCol>

      <CCol md="2">
        <CRow>
          <CCol md="12" class="d-grid gap-2 d-lg-block mb-3">
            <CButton color="primary" :disabled="disabled">회차추가</CButton>
          </CCol>
        </CRow>
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
import { maska } from 'maska'

export default defineComponent({
  name: 'PayOrderAddForm',
  directives: { maska },
  components: { ConfirmModal },
  data() {
    return {
      form: {
        pay_sort: '',
        pay_code: null,
        pay_time: null,
        pay_name: '',
        alias_name: '',
        is_pm_cost: false,
        pay_due_date: null,
        extra_due_date: null,
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
      this.form.pay_sort = ''
      this.form.pay_code = null
      this.form.pay_time = null
      this.form.pay_name = ''
      this.form.alias_name = ''
      this.form.is_pm_cost = false
      this.form.pay_due_date = null
      this.form.extra_due_date = null
    },
  },
})
</script>
