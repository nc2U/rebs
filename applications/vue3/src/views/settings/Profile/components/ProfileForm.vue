<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    enctype="multipart/form-data"
    @submit.prevent="onSubmit"
  >
    <CCardBody>
      <CRow class="flex-md-row flex-column-reverse">
        <CCol md="6">
          <CRow class="mb-3">
            <h6>사용자 계정</h6>
            <CFormLabel for="companyCeo" class="col-md-4 col-form-label">
              아이디
            </CFormLabel>

            <CCol md="8">
              {{ userInfo.username }}
              <CFormFeedback invalid>아이디를 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="companyName" class="col-md-4 col-form-label">
              이메일 주소
            </CFormLabel>

            <CCol md="8">
              {{ userInfo.email }}
              <CFormFeedback invalid>이메일을 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>

          <hr />

          <CRow class="mb-3">
            <h6>사용자 프로필</h6>
            <CFormLabel for="companyName" class="col-md-4 col-form-label">
              성명
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
              <DatePicker
                type="text"
                v-model="form.birth_date"
                v-maska="'####-##-##'"
                placeholder="생년월일을 입력하세요"
                maxlength="10"
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
                v-model="form.cell_phone"
                v-maska="['###-###-####', '###-####-####']"
                placeholder="휴대전화를 입력하세요"
                maxlength="13"
              />
              <CFormFeedback invalid>휴대전화를 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>
        </CCol>
        <CCol md="6">
          <AvatarInput
            v-model="form.image"
            :default-src="imgUrl"
            class="h-40 w-40 rounded-full"
            @file-upload="fileUpload"
          />
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
      <CButton type="submit" :color="btnClass" :disabled="pk && formsCheck">
        <CIcon name="cil-check-circle" />
        {{ confirmText }}
      </CButton>
    </CCardFooter>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>프로필 정보</template>
    <template v-slot:default>
      프로필 정보 {{ confirmText }}을 진행하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton :color="btnClass" @click="modalAction">
        {{ confirmText }}
      </CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import AvatarInput from './AvatarInput.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { maska } from 'maska'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ProfileForm',
  components: { AvatarInput, DatePicker, ConfirmModal, AlertModal },
  directives: { maska },
  props: {
    userInfo: Object,
  },
  data() {
    return {
      pk: '',
      form: {
        user: '',
        name: '',
        birth_date: '',
        cell_phone: '',
        // image: null,
      },
      validated: false,
    }
  },
  created(this: any) {
    if (this.userInfo) {
      this.pk = this.userInfo.profile.pk

      if (this.userInfo.profile) {
        this.form.user = this.userInfo.pk
        this.form.name = this.userInfo.profile.name
        this.form.birth_date = this.userInfo.profile.birth_date
        this.form.cell_phone = this.userInfo.profile.cell_phone
      }
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.name === this.userInfo.profile.name
      const b = this.form.birth_date === this.userInfo.profile.birth_date
      const c = this.form.cell_phone === this.userInfo.profile.cell_phone
      // const d = this.form.image === null
      return a && b && c // && d
    },
    imgUrl(this: any) {
      return this.userInfo &&
        this.userInfo.profile &&
        this.userInfo.profile.image
        ? this.userInfo.profile.image
        : '/static/dist/img/NoImage.jpeg'
    },
    confirmText(this: any) {
      return this.userInfo.profile.pk ? '변경' : '등록'
    },
    btnClass(this: any) {
      return this.userInfo.profile.pk ? 'success' : 'primary'
    },
    ...mapGetters('accounts', ['isAuthorized']),
  },
  methods: {
    fileUpload(image: any) {
      // this.form.image = image
      // console.log(image)
      this.$emit('file-upload', image)
    },
    onSubmit(this: any, event: any) {
      if (this.isAuthorized) {
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
      this.form.birth_date = this.dateFormat(this.form.birth_date)
      const payload = pk ? { ...{ pk }, ...this.form } : { ...this.form }
      this.$emit('on-submit', payload)
      this.validated = false
      this.$refs.confirmModal.visible = false
    },
  },
})
</script>
