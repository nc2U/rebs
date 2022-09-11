<script setup lang="ts">
import { ref, reactive, computed, onBeforeMount } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { Project } from '@/store/types/project'
import { callAddress, AddressData } from '@/components/DaumPostcode/address'
import DaumPostcode from '@/components/DaumPostcode/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  project: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['to-submit', 'reset-form', 'close'])

const accountStore = useAccount()

const form = reactive<Project>({
  pk: null,
  company: null,
  name: '',
  order: null,
  kind: '',
  start_year: '',
  is_direct_manage: false,
  is_returned_area: false,
  is_unit_set: false,
  local_zipcode: '',
  local_address1: '',
  local_address2: '',
  local_address3: '',
  area_usage: '',
  build_size: '',
  num_unit: null,
  buy_land_extent: null,
  scheme_land_extent: null,
  donation_land_extent: null,
  on_floor_area: null,
  under_floor_area: null,
  total_floor_area: null,
  build_area: null,
  floor_area_ratio: null,
  build_to_land_ratio: null,
  num_legal_parking: null,
  num_planed_parking: null,
})

const sortOptins = [
  { value: '1', label: '공동주택(아파트)' },
  { value: '2', label: '공동주택(타운하우스)' },
  { value: '3', label: '주상복합(아파트)' },
  { value: '4', label: '주상복합(오피스텔)' },
  { value: '5', label: '근린생활시설' },
  { value: '6', label: '생활형숙박시설' },
  { value: '7', label: '지식산업센터' },
  { value: '8', label: '기타' },
]

const validated = ref(false)

const confirmText = computed(() => (props.project ? '변경' : '등록'))
const btnClass = computed(() => (props.project ? 'success' : 'primary'))

const formsCheck = computed(() => {
  if (props.project) {
    const a = form.name === props.project.name
    const b = form.order === props.project.order
    const c = form.kind === props.project.kind
    const d = form.start_year === props.project.start_year
    const e = form.is_direct_manage === props.project.is_direct_manage
    const f = form.is_returned_area === props.project.is_returned_area
    const g = form.is_unit_set === props.project.is_unit_set
    const h = form.local_zipcode === props.project.local_zipcode
    const i = form.local_address1 === props.project.local_address1
    const j = form.local_address2 === props.project.local_address2
    const k = form.local_address3 === props.project.local_address3
    const l = form.area_usage === props.project.area_usage
    const m = form.build_size === props.project.build_size
    const n = form.num_unit === props.project.num_unit
    const o = form.buy_land_extent === props.project.buy_land_extent
    const p = form.scheme_land_extent === props.project.scheme_land_extent
    const q = form.donation_land_extent === props.project.donation_land_extent
    const r = form.on_floor_area === props.project.on_floor_area
    const s = form.under_floor_area === props.project.under_floor_area
    const t = form.total_floor_area === props.project.total_floor_area
    const u = form.build_area === props.project.build_area
    const v = form.floor_area_ratio === props.project.floor_area_ratio
    const w = form.build_to_land_ratio === props.project.build_to_land_ratio
    const x = form.num_legal_parking === props.project.num_legal_parking
    const y = form.num_planed_parking === props.project.num_planed_parking

    const group1 = a && b && c && d && e && f && g && h
    const group2 = i && j && k && l && m && n && o && p
    const group3 = q && r && s && t && u && v && w && x && y

    return group1 && group2 && group3
  } else return false
})

const delModal = ref()
const alertModal = ref()
const confirmModal = ref()
const address2 = ref()

const onSubmit = (event: Event) => {
  if (accountStore.superAuth) {
    const e = event.currentTarget as HTMLSelectElement
    if (!e.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()
      validated.value = true
    } else {
      confirmModal.value.callModal()
    }
  } else alertModal.value.callModal()
}

const modalAction = () => {
  if (form.order === null) form.order = 100
  emit('to-submit', { ...form })
  validated.value = false
  confirmModal.value.close()
}

const deleteProject = () => {
  if (accountStore.superAuth) delModal.value.callModal()
  else alertModal.value.callModal()
}

const addressCallback = (data: AddressData) => {
  const { formNum, zipcode, address1, address3 } = callAddress(data)
  if (formNum === 1) {
    // 입력할 데이터와 focus 폼 지정
    form.local_zipcode = zipcode
    form.local_address1 = address1
    form.local_address2 = ''
    form.local_address3 = address3
    address2.value.$el.nextElementSibling.focus()
  }
}

onBeforeMount(() => {
  if (props.project) {
    form.pk = props.project.pk
    form.company = props.project.company
    form.name = props.project.name
    form.order = props.project.order
    form.kind = props.project.kind
    form.start_year = props.project.start_year
    form.is_direct_manage = props.project.is_direct_manage
    form.is_returned_area = props.project.is_returned_area
    form.is_unit_set = props.project.is_unit_set
    form.local_zipcode = props.project.local_zipcode
    form.local_address1 = props.project.local_address1
    form.local_address2 = props.project.local_address2
    form.local_address3 = props.project.local_address3
    form.area_usage = props.project.area_usage
    form.build_size = props.project.build_size
    form.num_unit = props.project.num_unit
    form.buy_land_extent = props.project.buy_land_extent
    form.scheme_land_extent = props.project.scheme_land_extent
    form.donation_land_extent = props.project.donation_land_extent
    form.on_floor_area = props.project.on_floor_area
    form.under_floor_area = props.project.under_floor_area
    form.total_floor_area = props.project.total_floor_area
    form.build_area = props.project.build_area
    form.floor_area_ratio = props.project.floor_area_ratio
    form.build_to_land_ratio = props.project.build_to_land_ratio
    form.num_legal_parking = props.project.num_legal_parking
    form.num_planed_parking = props.project.num_planed_parking
  } else form.company = accountStore.staffAuth?.company || null
})
</script>

<template>
  <CCard>
    <CForm
      class="needs-validation"
      novalidate
      :validated="validated"
      @submit.prevent="onSubmit"
    >
      <CCardBody>
        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 프로젝트명</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.name"
              type="text"
              maxlength="30"
              placeholder="프로젝트명을 입력하세요"
              required
            />
            <CFormFeedback invalid>프로젝트명을 입력하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 정렬순서</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model.number="form.order"
              type="number"
              min="0"
              placeholder="프로젝트 정력순서를 입력하세요"
            />
            <CFormFeedback invalid>정렬순서를 입력하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 프로젝트종류</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormSelect v-model="form.kind" required>
              <option value="">프로젝트 종류</option>
              <option
                v-for="sort in sortOptins"
                :key="sort.value"
                :value="sort.value"
                :selected="update && sort.value === project.kind"
              >
                {{ sort.label }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>프로젝트종류를 선택하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 사업개시년도</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model.number="form.start_year"
              type="number"
              min="1990"
              placeholder="사업개시년도를 입력하세요"
              required
            />
            <CFormFeedback invalid>
              사업개시년도를 입력하세요(1990년도 이후).
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"></CFormLabel>
          <CCol md="8" lg="5">
            <CFormSwitch
              id="is_direct_manage"
              v-model="form.is_direct_manage"
              label="직영운영여부"
              :checked="update && project.is_direct_manage"
            />
            <CFormText class="text-grey">
              본사 직접 운영하는 프로젝트인 경우 체크, 즉 시행대행이나
              업무대행이 아닌 경우
            </CFormText>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"></CFormLabel>
          <CCol md="8" lg="5">
            <CFormSwitch
              id="is_returned_area"
              v-model="form.is_returned_area"
              label="토지환지여부"
              :checked="update && project.is_returned_area"
            />
            <CFormText class="text-grey">
              해당 사업부지가 환지방식 도시개발사업구역인 경우 체크
            </CFormText>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"></CFormLabel>
          <CCol md="8" lg="5">
            <CFormSwitch
              id="is_unit_set"
              v-model="form.is_unit_set"
              label="동호지정여부"
              :checked="update && project.is_unit_set"
            />
            <CFormText class="text-grey">
              현재 동호수를 지정하지 않는 경우 체크하지 않음
            </CFormText>
          </CCol>
        </CRow>
        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 우편번호</CFormLabel>
          <CCol md="3" lg="2" class="mb-3 mb-lg-0">
            <CInputGroup>
              <CInputGroupText @click="$refs.postCode.initiate()">
                우편번호
              </CInputGroupText>
              <CFormInput
                v-model="form.local_zipcode"
                type="text"
                maxlength="5"
                placeholder="우편번호"
                @focus="$refs.postCode.initiate()"
              />
              <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>
            </CInputGroup>
          </CCol>

          <CCol md="7" lg="4" class="mb-3 mb-lg-0">
            <CFormInput
              v-model="form.local_address1"
              type="text"
              maxlength="50"
              placeholder="대표지번 주소를 입력하세요"
              @focus="$refs.postCode.initiate()"
            />
            <CFormFeedback invalid>대표지번 주소를 입력하세요.</CFormFeedback>
          </CCol>

          <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

          <CCol md="5" lg="2" class="mb-3 mb-lg-0">
            <CFormInput
              ref="address2"
              v-model="form.local_address2"
              type="text"
              maxlength="25"
              placeholder="상세주소를 입력하세요"
            />
            <CFormFeedback invalid>상세주소를 입력하세요.</CFormFeedback>
          </CCol>
          <CCol md="5" lg="2">
            <CFormInput
              v-model="form.local_address3"
              type="text"
              maxlength="20"
              placeholder="참고항목을 입력하세요"
            />
            <CFormFeedback invalid>참고항목을 입력하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 용도지역지구</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.area_usage"
              type="text"
              maxlength="50"
              placeholder="용도지역지구를 입력하세요"
              required
            />
            <CFormFeedback invalid>용도지역지구를 입력하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 건축규모</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.build_size"
              type="text"
              maxlength="50"
              placeholder="건축규모를 입력하세요"
              required
            />
            <CFormFeedback invalid>건축규모를 입력하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label">
            세대(호/실)수
          </CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model.number="form.num_unit"
              type="number"
              min="0"
              placeholder="세대(호/실)수를 입력하세요"
            />
            <CFormFeedback invalid>세대(호/실)수를 입력하세요.</CFormFeedback>
          </CCol>
          <CFormLabel class="col-md-2 col-form-label"> 대지매입면적</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model.number="form.buy_land_extent"
              type="number"
              min="0"
              step="0.0001"
              placeholder="대지매입면적을 입력하세요"
            />
            <CFormFeedback invalid>
              대지매입면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 계획대지면적</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model.number="form.scheme_land_extent"
              type="number"
              min="0"
              step="0.0001"
              placeholder="계획대지면적을 입력하세요"
            />
            <CFormFeedback invalid>
              계획대지면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 기부채납면적</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model.number="form.donation_land_extent"
              type="number"
              min="0"
              step="0.0001"
              placeholder="기부채납면적을 입력하세요"
            />
            <CFormFeedback invalid>
              기부채납면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 지상연면적</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model.number="form.on_floor_area"
              type="number"
              min="0"
              step="0.0001"
              placeholder="지상연면적을 입력하세요"
            />
            <CFormFeedback invalid>
              지상연면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 지하연면적</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model.number="form.under_floor_area"
              type="number"
              min="0"
              step="0.0001"
              placeholder="지하연면적을 입력하세요"
            />
            <CFormFeedback invalid>
              지하연면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 총 연면적</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model.number="form.total_floor_area"
              type="number"
              min="0"
              step="0.0001"
              placeholder="총 연면적을 입력하세요"
            />
            <CFormFeedback invalid>
              총 연면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 건축면적</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model.number="form.build_area"
              type="number"
              min="0"
              step="0.0001"
              placeholder="건축면적을 입력하세요"
            />
            <CFormFeedback invalid>
              총 연면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 용적율(%)</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model.number="form.floor_area_ratio"
              type="number"
              min="0"
              step="0.0001"
              placeholder="용적율(%)을 입력하세요"
            />
            <CFormFeedback invalid>
              용적율(%)을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
          <CFormLabel class="col-md-2 col-form-label"> 건폐율(%)</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model.number="form.build_to_land_ratio"
              type="number"
              min="0"
              step="0.0001"
              placeholder="건폐율(%)을 입력하세요"
            />
            <CFormFeedback invalid>
              건폐율(%)을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 법정주차대수</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model.number="form.num_legal_parking"
              type="number"
              min="0"
              placeholder="법정주차대수를 입력하세요"
            />
            <CFormFeedback invalid>법정주차대수를 입력하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 계획주차대수</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model.number="form.num_planed_parking"
              type="number"
              min="0"
              placeholder="계획주차대수를 입력하세요"
            />
            <CFormFeedback invalid>계획주차대수를 입력하세요.</CFormFeedback>
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
          @click="deleteProject"
        >
          삭제
        </CButton>
        <CButton type="submit" :color="btnClass" :disabled="formsCheck">
          <CIcon name="cil-check-circle" />
          저장
        </CButton>
      </CCardFooter>
    </CForm>
  </CCard>

  <DaumPostcode ref="postCode" @address-callback="addressCallback" />

  <ConfirmModal ref="delModal">
    <template #header>
      <CIcon name="cilChevronCircleRightAlt" />
      프로젝트정보 삭제
    </template>
    <template #default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template #footer>
      <CButton color="danger" disabled="">삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cilChevronCircleRightAlt" />
      프로젝트정보
    </template>
    <template #default>
      프로젝트정보 {{ confirmText }}을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
