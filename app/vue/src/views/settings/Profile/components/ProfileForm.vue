<script lang="ts" setup>
import { reactive, ref, computed, onBeforeMount, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { maska as vMaska } from 'maska'
import { dateFormat } from '@/utils/baseMixins'
import { Profile } from '@/store/types/accounts'
import DatePicker from '@/components/DatePicker/index.vue'
import AvatarInput from './AvatarInput.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  profile: { type: Object, default: null },
})

const emit = defineEmits(['file-upload', 'on-submit', 'reset-form'])

const alertModal = ref()
const confirmModal = ref()

const form = reactive<Profile>({
  pk: null,
  user: null,
  name: '',
  birth_date: '',
  cell_phone: '',
  image: '',
})

watch(form, val => {
  if (val.birth_date) form.birth_date = dateFormat(val.birth_date)
})

const validated = ref(false)

const accountStore = useAccount()
const userInfo = computed(() => accountStore.userInfo)

const formsCheck = computed(() => (props.profile?.pk ? isChanged() : false))

const confirmText = computed(() => (props.profile?.pk ? '변경' : '등록'))

const btnClass = computed(() => (props.profile?.pk ? 'success' : 'primary'))

const isChanged = () => {
  const a = form.name === props.profile.name
  const b = form.birth_date === props.profile.birth_date
  const c = form.cell_phone === props.profile.cell_phone
  const d = !form.image || form.image === props.profile.image
  return a && b && c && d
}

const fileUpload = (img: File) => (form.image = img.name)

const onSubmit = (event: Event) => {
  if (userInfo.value) {
    const e = event.currentTarget as HTMLSelectElement
    if (!e.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else {
      confirmModal.value.callModal()
    }
  } else {
    alertModal.value.callModal()
  }
}

const modalAction = () => {
  emit('on-submit', form)
  validated.value = false
  confirmModal.value.close()
}

const resetForm = () => {
  if (props.profile) {
    if (props.profile) {
      form.pk = props.profile.pk
      form.user = props.profile.user
      form.name = props.profile.name
      form.birth_date = props.profile.birth_date
      form.cell_phone = props.profile.cell_phone
      form.image = props.profile.image
    }
  } else {
    form.pk = null
    form.user = null
    form.name = ''
    form.birth_date = ''
    form.cell_phone = ''
    form.image = ''
  }
}

onBeforeMount(() => resetForm())
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
        <CCol md="6">
          <CRow class="mb-3">
            <h6>사용자 계정</h6>
            <CFormLabel for="companyCeo" class="col-md-4 col-form-label">
              아이디
            </CFormLabel>

            <CCol md="8">
              {{ userInfo?.username || '' }}
              <CFormFeedback invalid>아이디를 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="companyName" class="col-md-4 col-form-label">
              이메일 주소
            </CFormLabel>

            <CCol md="8">
              {{ userInfo?.email || '' }}
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
                v-model="form.name"
                type="text"
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
                v-model="form.birth_date"
                v-maska="'####-##-##'"
                type="text"
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
                v-model="form.cell_phone"
                v-maska="['###-###-####', '###-####-####']"
                type="text"
                placeholder="휴대전화를 입력하세요"
                maxlength="13"
              />
              <CFormFeedback invalid>휴대전화를 입력하세요.</CFormFeedback>
            </CCol>
          </CRow>
        </CCol>
        <CCol md="6">
          <AvatarInput
            ref="avatar"
            :default-src="form.image"
            @file-upload="fileUpload"
          />
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter class="text-right">
      <CButton type="button" color="light" @click="resetForm"> 취소</CButton>
      <CButton type="submit" :color="btnClass" :disabled="formsCheck">
        <CIcon name="cil-check-circle" />
        {{ confirmText }}
      </CButton>
    </CCardFooter>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header>프로필 정보</template>
    <template #default>
      프로필 정보 {{ confirmText }}을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton :color="btnClass" @click="modalAction">
        {{ confirmText }}
      </CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
