<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CCardBody>
      <CRow class="flex-md-row flex-column-reverse">
        <CCol md="6">
          <CRow class="mb-3">
            <h6>사용자 계정</h6>
            <CFormLabel for="companyCeo" class="col-md-4 col-form-label">
              아 이 디
            </CFormLabel>

            <CCol md="8">
              <CFormInput
                type="text"
                v-model="form.ceo"
                placeholder="아이디를 입력하세요"
                maxlength="20"
                required
              />
              <CFormFeedback invalid>아이디를 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="companyName" class="col-md-4 col-form-label">
              이메일 주소
            </CFormLabel>

            <CCol md="8">
              <CFormInput
                type="text"
                v-model="form.name"
                placeholder="이메일을 입력하세요"
                maxlength="20"
                required
              />
              <CFormFeedback invalid>이메일을 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>

          <hr />
          <CRow class="mb-3">
            <h6>사용자 프로필</h6>
            <CFormLabel for="companyName" class="col-md-4 col-form-label">
              성 명
            </CFormLabel>

            <CCol md="8">
              <CFormInput
                type="text"
                v-model="form.name"
                placeholder="성명을 입력하세요"
                maxlength="20"
                required
              />
              <CFormFeedback invalid>성명을 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>
          <CRow class="mb-3">
            <CFormLabel for="companyCeo" class="col-md-4 col-form-label">
              생년월일
            </CFormLabel>

            <CCol md="8">
              <CFormInput
                type="text"
                v-model="form.ceo"
                placeholder="생년월일을 입력하세요"
                maxlength="20"
                required
              />
              <CFormFeedback invalid>생년월일을 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="companyCeo" class="col-md-4 col-form-label">
              휴대전화
            </CFormLabel>

            <CCol md="8">
              <CFormInput
                type="text"
                v-model="form.ceo"
                placeholder="휴대전화를 입력하세요"
                maxlength="20"
                required
              />
              <CFormFeedback invalid>휴대전화를 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>
        </CCol>
        <CCol md="6">
          <CRow class="mb-4">
            <CCol>
              <h6>Profile picture</h6>
              <CImage
                rounded
                thumbnail
                fluid
                src="https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/users/no-image.jpeg"
                width="200"
                height="200"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter class="text-right">
      <CButton type="button" color="light" @click="this.$emit('reset-form')">
        취소
      </CButton>
      <CButton
        type="button"
        v-if="update"
        color="danger"
        @click="deleteCompany"
      >
        삭제
      </CButton>
      <CButton type="submit" :color="btnClass" :disabled="formsCheck">
        <CIcon name="cil-check-circle" />
        저장
      </CButton>
    </CCardFooter>
  </CForm>

  <DaumPostcode @addressPut="addressPut" ref="postCode" />

  <ConfirmModal ref="delModal">
    <template v-slot:header>회사정보</template>
    <template v-slot:default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template v-slot:footer>
      <CButton color="danger" disabled="">삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>회사정보</template>
    <template v-slot:default>
      회사정보 {{ confirmText }}을 진행하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
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
  name: 'ProfileForm',
  components: { ConfirmModal, AlertModal },
  data() {
    return {
      pk: '',
      form: {
        name: '',
        ceo: '',
      },
      validated: false,
    }
  },
  created() {
    if (this.company) {
      this.pk = this.company.pk
      this.form.name = this.company.name
    }
  },
  props: {
    company: Object,
  },
  computed: {
    formsCheck(this: any) {
      // const a = this.form.name === this.company.name
      // const b = this.form.ceo === this.company.ceo
      return 1 //a && b
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    onSubmit(this: any, event: any) {
      if (this.writeAuth) {
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
      }
    },
    modalAction(this: any) {
      const { pk } = this
      if (this.update) {
        this.$emit('to-update', { ...{ pk }, ...this.form })
      } else {
        this.$emit('to-create', this.form)
      }
      this.validated = false
    },
    deleteCompany(this: any) {
      if (this.superAuth) this.$refs.delModal.callModal()
      else this.$refs.alertModal.callModal()
    },
  },
})
</script>

<style lang="scss" scoped>
@media (min-width: 768px) {
  .flex-md-row {
    flex-direction: row !important;
  }
}

.flex-column-reverse {
  flex-direction: column-reverse;
}
</style>
