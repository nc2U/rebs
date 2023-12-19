<script lang="ts" setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { type Profile } from '@/store/types/accounts'
import DatePicker from '@/components/DatePicker/index.vue'
import AvatarInput from './AvatarInput.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  profile: { type: Object, default: null },
})

const emit = defineEmits(['on-submit', 'reset-form'])

const refAlertModal = ref()
const refConfirmModal = ref()

const form = reactive<Profile>({
  pk: null,
  user: null,
  name: '',
  birth_date: '',
  cell_phone: '',
  image: undefined,
})

const validated = ref(false)

const accountStore = useAccount()
const userInfo = computed(() => accountStore.userInfo)

const formsCheck = computed(() => {
  if (props.profile) {
    const a = form.name === props.profile.name
    const b = form.birth_date === props.profile.birth_date
    const c = form.cell_phone === props.profile.cell_phone
    const d = !form.image || form.image === props.profile.image
    return a && b && c && d
  } else return false
})

const confirmText = computed(() => (props.profile?.pk ? '변경' : '등록'))
const btnClass = computed(() => (props.profile?.pk ? 'success' : 'primary'))

const transProfileForm = (img: File) => (form.image = img)

const onSubmit = (event: Event) => {
  if (userInfo.value) {
    const e = event.currentTarget as HTMLSelectElement
    if (!e.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else {
      refConfirmModal.value.callModal()
    }
  } else {
    refAlertModal.value.callModal()
  }
}

const modalAction = () => {
  emit('on-submit', form)
  validated.value = false
  refConfirmModal.value.close()
}

const formDataReset = () => {
  form.pk = null
  form.user = null
  form.name = ''
  form.birth_date = ''
  form.cell_phone = ''
  form.image = undefined
}

const formDataSetup = () => {
  if (props.profile) {
    form.pk = props.profile.pk
    form.user = props.profile.user
    form.name = props.profile.name
    form.birth_date = props.profile.birth_date
    form.cell_phone = props.profile.cell_phone
  }
}

onMounted(() => formDataSetup())
</script>

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
        <CCol md="4">
          <CRow class="mb-3">
            <h6>사용자 계정</h6>
            <CFormLabel class="col-sm-4 col-form-label"> 아이디</CFormLabel>

            <CCol sm="8">{{ userInfo?.username || '' }}</CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel class="col-sm-4 col-form-label"> 이메일 주소</CFormLabel>

            <CCol sm="8">{{ userInfo?.email || '' }}</CCol>
          </CRow>

          <v-divider class="my-4" />

          <CRow class="mb-3">
            <h6>사용자 프로필</h6>
            <CFormLabel for="name" class="col-sm-4 col-form-label"> 성명</CFormLabel>

            <CCol sm="8">
              <CFormInput
                v-model="form.name"
                type="text"
                placeholder="성명을 입력하세요"
                maxlength="20"
                id="name"
                required
              />
              <CFormFeedback invalid>성명을 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>
          <CRow class="mb-3">
            <CFormLabel for="birth_date" class="col-sm-4 col-form-label"> 생년월일</CFormLabel>

            <CCol sm="8">
              <DatePicker
                v-model="form.birth_date"
                placeholder="생년월일을 입력하세요"
                maxlength="10"
                id="birth_date"
              />
              <CFormFeedback invalid>생년월일을 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="cell_phone" class="col-sm-4 col-form-label"> 휴대전화</CFormLabel>

            <CCol sm="8">
              <input
                v-model="form.cell_phone"
                v-maska
                data-maska="['###-###-####', '###-####-####']"
                type="text"
                class="form-control"
                placeholder="휴대전화를 입력하세요"
                maxlength="13"
                id="cell_phone"
              />
              <CFormFeedback invalid>휴대전화를 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>
        </CCol>
        <CCol md="8">
          <AvatarInput
            ref="avatar"
            :image="(profile && profile.image) || '/static/dist/img/NoImage.jpeg'"
            @trans-profile-form="transProfileForm"
          />
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter class="text-right">
      <CButton type="button" color="light" @click="formDataReset"> 취소</CButton>
      <CButton type="submit" :color="btnClass" :disabled="formsCheck">
        <CIcon name="cil-check-circle" />
        {{ confirmText }}
      </CButton>
    </CCardFooter>
  </CForm>

  <ConfirmModal ref="refConfirmModal">
    <template #header>프로필 정보</template>
    <template #default> 프로필 정보 {{ confirmText }}을 진행하시겠습니까?</template>
    <template #footer>
      <CButton :color="btnClass" @click="modalAction">
        {{ confirmText }}
      </CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="refAlertModal" />
</template>
