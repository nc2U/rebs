<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CModalBody class="p-4">
      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">계약자</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.contractor" required readonly>
                <option>
                  {{ contractorName }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label"> 구분</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.status" required>
                <option value="">---------</option>
                <option value="0" v-if="release && release.status < '4'">
                  신청 취소
                </option>
                <option value="3" v-if="!release">해지 신청</option>
                <option value="4">해지 종결</option>
                <option value="5">자격 상실(제명)</option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              환불(예정)금액
            </CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.refund_amount"
                type="number"
                min="0"
                placeholder="환불(예정)금액"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              환불계좌(은행)
            </CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.refund_account_bank"
                placeholder="환불계좌(은행)"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              환불계좌(번호)
            </CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.refund_account_number"
                placeholder="환불계좌(번호)"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              환불계좌(예금주)
            </CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.refund_account_depositor"
                placeholder="환불계좌(예금주)"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label"> 해지신청일</CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="form.request_date"
                required
                placeholder="해지신청일"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              해지(환불)처리일
            </CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="form.completion_date"
                :required="false"
                placeholder="해지종결일"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol>
          <CRow>
            <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
            <CCol sm="10">
              <CFormTextarea v-model="form.note" placeholder="기타 특이사항" />
            </CCol>
          </CRow>
        </CCol>
      </CRow>
    </CModalBody>

    <CModalFooter>
      <CButton type="button" color="light" @click="$emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          :color="release ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="release"
          type="button"
          color="danger"
          @click="deleteConfirm"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>
  </CForm>

  <!--  <ConfirmModal ref="confirmModal">-->
  <!--    <template v-slot:header>-->
  <!--      <CIcon name="cil-warning" />-->
  <!--      건별 수납 정보 - [삭제]-->
  <!--    </template>-->
  <!--    <template v-slot:default>-->
  <!--      삭제 후 복구할 수 없습니다. 해당 건별 수납 정보 삭제를 진행하시겠습니까?-->
  <!--    </template>-->
  <!--    <template v-slot:footer>-->
  <!--      <CButton color="danger" @click="modalAction">삭제</CButton>-->
  <!--    </template>-->
  <!--  </ConfirmModal>-->

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
// import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ContCancelForm',
  components: {
    DatePicker,
    // ConfirmModal,
    AlertModal,
  },
  props: { release: Object, contractor: Object },
  data() {
    return {
      form: {
        contractor: '',
        status: '',
        refund_amount: '',
        refund_account_bank: '',
        refund_account_number: '',
        refund_account_depositor: '',
        request_date: '',
        completion_date: '',
        note: '',
      },
      validated: false,
    }
  },
  created(this: any) {
    if (this.release && this.release.pk) {
      this.form.contractor = this.contractorName
      this.form.status = this.release.status
      this.form.refund_amount = this.release.refund_amount
      this.form.refund_account_bank = this.release.refund_account_bank
      this.form.refund_account_number = this.release.refund_account_number
      this.form.refund_account_depositor = this.release.refund_account_depositor
      this.form.request_date = this.release.request_date
      this.form.completion_date = this.release.completion_date
      this.form.note = this.release.note
    }
  },
  computed: {
    contractorName(this: any) {
      let name = ''
      if (this.release) name = this.release.contractor.name
      if (this.contractor) name = this.contractor.name
      return name
    },
    pageManageAuth() {
      return (
        this.superAuth || (this.staffAuth && this.staffAuth.releaseract === '2')
      )
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    onSubmit(this: any, event: any) {
      if (this.pageManageAuth) {
        const form = event.currentTarget
        if (form.checkValidity() === false) {
          event.preventDefault()
          event.stopPropagation()

          this.validated = true
        } else {
          this.$emit('on-submit', this.form)
        }
      } else this.$refs.alertModal.callModal()
    },
    deleteConfirm() {
      alert('delete ready!')
    },
  },
})
</script>
