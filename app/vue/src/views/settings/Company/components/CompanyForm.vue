<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useAccount } from '@/store/pinia/accounts'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import DaumPostcode from '@/components/DaumPostcode/index.vue'
// import { addressPut } from '@/components/DaumPostcode/address'
import { dateFormat } from '@/utils/baseMixins'
import { maska as vMaska } from 'maska'

const account = useAccount()

const props = defineProps({
  company: { type: Object, default: null },
  update: { type: Boolean, required: true },
})

const delModal = ref()
const alertModal = ref()
const confirmModal = ref()
const postCode = ref()
const address2 = ref()

const pk = ref('')
const validated = ref(false)
const form = ref({
  name: '',
  ceo: '',
  tax_number: '',
  org_number: '',
  business_cond: '',
  business_even: '',
  es_date: new Date() as string | Date,
  op_date: new Date() as string | Date,
  zipcode: '',
  address1: '',
  address2: '',
  address3: '',
})

const addressPut = (data: any) => {
  // form.value.addrForm = data.formNum
  form.value.zipcode = data.zonecode

  if (data.userSelectedType === 'R') {
    form.value.address1 = data.roadAddress // 사용자가 도로명 주소를 선택했을 경우
  } else {
    form.value.address1 = data.jibunAddress // 사용자가 지번 주소를 선택했을 경우(J)
  }

  if (data.userSelectedType === 'R') {
    // 법정동명이 있을 경우 추가한다. (법정리는 제외), 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
    if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
      form.value.address3 = data.bname
    }

    if (data.buildingName !== '' && data.apartment === 'Y') {
      // 건물명이 있고, 공동주택일 경우 추가한다.
      form.value.address3 +=
        form.value.address3 !== ''
          ? ', ' + data.buildingName
          : data.buildingName
    }
    // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
    if (form.value.address3 !== '') {
      form.value.address3 = ' (' + form.value.address3 + ')'
    }
  }
  form.value.address2 = ''
  address2.value.$el.nextElementSibling.focus()
}

const onSubmit = (event: any) => {
  if (writeAuth.value) {
    const form = event.currentTarget
    if (form.checkValidity() === false) {
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

const emit = defineEmits(['to-create', 'to-update', 'reset-form'])

const modalAction = () => {
  form.value.es_date = dateFormat(new Date(form.value.es_date))
  form.value.op_date = dateFormat(new Date(form.value.op_date))

  if (props.update) {
    emit('to-update', { ...{ pk }, ...form.value })
  } else {
    emit('to-create', form.value)
  }
  validated.value = false
}

const deleteCompany = () => {
  if (account.superAuth) delModal.value.callModal()
  else alertModal.value.callModal()
}

const confirmText = computed(() => (props.update ? '변경' : '등록'))
const btnClass = computed(() => (props.update ? 'success' : 'primary'))

const formsCheck = computed(() => {
  const a = form.value.name === props.company.name
  const b = form.value.ceo === props.company.ceo
  const c = form.value.tax_number === props.company.tax_number
  const d = form.value.org_number === props.company.org_number
  const e = form.value.business_cond === props.company.business_cond
  const f = form.value.business_even === props.company.business_even
  const g =
    new Date(form.value.es_date).toString() ===
    new Date(props.company.es_date).toString()
  const h =
    new Date(form.value.op_date).toString() ===
    new Date(props.company.op_date).toString()
  const i = form.value.zipcode === props.company.zipcode
  const j = form.value.address1 === props.company.address1
  const k = form.value.address2 === props.company.address2
  const l = form.value.address3 === props.company.address3

  return a && b && c && d && e && f && g && h && i && j && k && l
})

const writeAuth = computed(() => {
  const create = !!account.superAuth
  const update =
    account.superAuth ||
    (account.staffAuth && account.staffAuth.company_settings === '2')
  return props.update ? update : create
})

onBeforeMount(() => {
  if (props.update && props.company) {
    pk.value = props.company.pk
    form.value.name = props.company.name
    form.value.ceo = props.company.ceo
    form.value.tax_number = props.company.tax_number
    form.value.org_number = props.company.org_number
    form.value.business_cond = props.company.business_cond
    form.value.business_even = props.company.business_even
    form.value.es_date = new Date(props.company.es_date)
    form.value.op_date = new Date(props.company.op_date)
    form.value.zipcode = props.company.zipcode
    form.value.address1 = props.company.address1
    form.value.address2 = props.company.address2
    form.value.address3 = props.company.address3
  }
})
</script>

<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CCardBody>
      <CRow class="mb-3">
        <CFormLabel for="companyName" class="col-md-2 col-form-label">
          회사명
        </CFormLabel>

        <CCol md="4">
          <CFormInput
            v-model="form.name"
            type="text"
            placeholder="회사명을 입력하세요"
            maxlength="20"
            required
          />
          <CFormFeedback invalid>회사명을 입력하세요.</CFormFeedback>
        </CCol>

        <CFormLabel for="companyCeo" class="col-md-2 col-form-label">
          대표자명
        </CFormLabel>

        <CCol md="4">
          <CFormInput
            v-model="form.ceo"
            type="text"
            placeholder="대표자명을 입력하세요"
            maxlength="20"
            required
          />
          <CFormFeedback invalid>대표자명을 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="taxNumber" class="col-md-2 col-form-label">
          사업자등록번호
        </CFormLabel>
        <CCol md="4">
          <CFormInput
            v-model="form.tax_number"
            v-maska="'###-##-#####'"
            type="text"
            placeholder="사업자번호를 입력하세요"
            maxlength="12"
            required
          />
          <CFormFeedback invalid>사업자등록번호를 입력하세요.</CFormFeedback>
        </CCol>
        <CFormLabel for="orgNumber" class="col-md-2 col-form-label">
          법인등록번호
        </CFormLabel>
        <CCol md="4">
          <CFormInput
            v-model="form.org_number"
            v-maska="'######-#######'"
            type="text"
            placeholder="법인등록번호를 입력하세요"
            maxlength="14"
            required
          />
          <CFormFeedback invalid>법인등록번호를 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="businessCond" class="col-md-2 col-form-label">
          업태
        </CFormLabel>
        <CCol md="4">
          <CFormInput
            v-model="form.business_cond"
            type="text"
            placeholder="업태를 입력하세요"
            maxlength="20"
            required
          />
          <CFormFeedback invalid>업태를 입력하세요.</CFormFeedback>
        </CCol>
        <CFormLabel for="businessEven" class="col-md-2 col-form-label">
          종목
        </CFormLabel>
        <CCol md="4">
          <CFormInput
            v-model="form.business_even"
            type="text"
            placeholder="종목을 입력하세요"
            maxlength="20"
            required
          />
          <CFormFeedback invalid>종목을 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="esDate" class="col-md-2 col-form-label">
          설립일자
        </CFormLabel>
        <CCol md="4">
          <DatePicker
            v-model="form.es_date"
            v-maska="'####-##-##'"
            type="text"
            maxlength="10"
            placeholder="설립일자를 입력하세요"
            required
          />
          <CFormFeedback invalid>설립일자를 입력하세요.</CFormFeedback>
        </CCol>
        <CFormLabel for="opDate" class="col-md-2 col-form-label">
          개업일자
        </CFormLabel>
        <CCol md="4">
          <DatePicker
            v-model="form.op_date"
            v-maska="'####-##-##'"
            type="text"
            maxlength="10"
            placeholder="개업일자를 입력하세요"
            required
          />
          <CFormFeedback invalid>개업일자를 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>

      <hr />

      <CRow>
        <CFormLabel for="zipcode" class="col-md-2 col-form-label">
          회사주소
        </CFormLabel>
        <CCol md="4" xl="2" class="mb-3">
          <CInputGroup>
            <CFormInput
              v-model="form.zipcode"
              type="text"
              placeholder="우편번호"
              maxlength="5"
              required
              @focus="postCode.initiate()"
            />
            <CInputGroupText @click="postCode.initiate()">
              우편번호
            </CInputGroupText>
            <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>
          </CInputGroup>
        </CCol>
      </CRow>
      <CRow>
        <CCol sm="2"></CCol>
        <CCol md="10" lg="4" class="mb-3">
          <CFormInput
            v-model="form.address1"
            type="text"
            placeholder="회사주소를 입력하세요"
            maxlength="50"
            required
            @focus="postCode.initiate()"
          />
          <CFormFeedback invalid>회사주소를 입력하세요.</CFormFeedback>
        </CCol>
        <CCol xs="2" class="d-none d-md-block d-lg-none"></CCol>
        <CCol md="5" lg="3" class="mb-3">
          <CFormInput
            ref="address2"
            v-model="form.address2"
            type="text"
            placeholder="상세주소를 입력하세요"
            maxlength="30"
            required
          />
          <CFormFeedback invalid>상세주소를 입력하세요.</CFormFeedback>
        </CCol>
        <CCol md="5" lg="3" class="mb-3">
          <CFormInput
            v-model="form.address3"
            type="text"
            placeholder="나머지 주소를 입력하세요"
            maxlength="30"
          />
          <CFormFeedback invalid>나머지 주소를 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter class="text-right">
      <CButton type="button" color="light" @click="emit('reset-form')">
        취소
      </CButton>
      <CButton
        v-if="update"
        type="button"
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

  <DaumPostcode ref="postCode" @address-put="addressPut" />

  <ConfirmModal ref="delModal">
    <template #header>
      <CIcon name="cilChevronCircleRightAlt" />
      회사정보
    </template>
    <template #default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template #footer>
      <CButton color="danger" disabled="">삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cilChevronCircleRightAlt" />
      회사정보
    </template>
    <template #default>
      회사정보 {{ confirmText }}을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
