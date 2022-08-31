<script lang="ts" setup>
import { ref, reactive, computed, watch, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { dateFormat } from '@/utils/baseMixins'
import { write_project } from '@/utils/pageAuth'
import { isValidate } from '@/utils/helper'
import { maska as vMaska } from 'maska'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import DaumPostcode from '@/components/DaumPostcode/index.vue'
import { AddressData, callAddress } from '@/components/DaumPostcode/address'

const props = defineProps({
  owner: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()
const postCode = ref()
const address2 = ref()

const validated = ref(false)

const pk = ref<number | null>(null)
const form = reactive({
  project: null as number | null,
  own_sort: '1',
  owner: '',
  date_of_birth: null as string | null,
  sites: [] as number[],
  relations: [] as number[],
  phone1: '',
  phone2: '',
  zipcode: '',
  address1: '',
  address2: '',
  address3: '',
  own_sort_desc: '',
  counsel_record: '',
})

const own_sort_select = [
  { val: '1', text: '개인' },
  { val: '2', text: '법인' },
  { val: '3', text: '국공유지' },
]

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const siteStore = useSite()
const getSites = computed(() => siteStore.getSites)

const formsCheck = computed(() => {
  if (props.owner) {
    const a = form.project === props.owner.project
    const b = form.own_sort === props.owner.own_sort
    const c = form.owner === props.owner.owner
    const d = form.date_of_birth === props.owner.date_of_birth
    const e = form.sites === props.owner.sites
    const f = form.phone1 === props.owner.phone1
    const g = form.phone2 === props.owner.phone2
    const h = form.zipcode === props.owner.zipcode
    const i = form.address1 === props.owner.address1
    const j = form.address2 === props.owner.address2
    const k = form.address3 === props.owner.address3
    const l = form.own_sort_desc === props.owner.own_sort_desc
    const m = form.counsel_record === props.owner.counsel_record

    return a && b && c && d && e && f && g && h && i && j && k && l && m
  } else return false
})

watch(form, val => {
  if (val.date_of_birth) form.date_of_birth = dateFormat(val.date_of_birth)
})

const addressCallback = (data: AddressData) => {
  const { formNum, zipcode, address1, address3 } = callAddress(data)
  if (formNum === 1) {
    // 입력할 데이터와 focus 폼 지정
    form.zipcode = zipcode
    form.address1 = address1
    form.address2 = ''
    form.address3 = address3
    address2.value.$el.nextElementSibling.focus()
  }
}

const onSubmit = (event: any) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    const payload = props.owner ? { pk: pk.value, ...form } : { ...form }
    if (write_project) multiSubmit(payload)
    else alertModal.value.callModal()
  }
}

const multiSubmit = (multiPayload: any) => {
  emit('multi-submit', multiPayload)
  emit('close')
}

const deleteObject = () => {
  emit('on-delete', { pk: props.owner.pk, project: props.owner.project })
  delModal.value.visible = false
  emit('close')
}

const deleteConfirm = () => {
  if (write_project) delModal.value.callModal()
  else alertModal.value.callModal()
}

onBeforeMount(() => {
  if (props.owner) {
    pk.value = props.owner.pk
    form.project = props.owner.project
    form.own_sort = props.owner.own_sort
    form.owner = props.owner.owner
    form.date_of_birth = props.owner.date_of_birth
    form.sites = props.owner.sites
    form.relations = props.owner.relations
    form.phone1 = props.owner.phone1
    form.phone2 = props.owner.phone2
    form.zipcode = props.owner.zipcode
    form.address1 = props.owner.address1
    form.address2 = props.owner.address2
    form.address3 = props.owner.address3
    form.own_sort_desc = props.owner.own_sort_desc
    form.counsel_record = props.owner.counsel_record
  } else {
    form.project = project.value
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
    <CModalBody class="p-4">
      <div>
        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">소유구분</CFormLabel>
              <CCol sm="8">
                <CFormSelect v-model="form.own_sort">
                  <option
                    v-for="sort in own_sort_select"
                    :key="sort.val"
                    :value="sort.val"
                  >
                    {{ sort.text }}
                  </option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label"> 소유자</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.owner"
                  required
                  placeholder="소유자"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">생년월일</CFormLabel>
              <CCol sm="8">
                <DatePicker
                  v-model="form.date_of_birth"
                  :required="false"
                  placeholder="생년월일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">
                {{ form.sites }} 소유지번 (<span class="text-bg-">필수</span>)
              </CFormLabel>
              <CCol sm="10">
                <select
                  v-model="form.sites"
                  required
                  multiple
                  class="form-control"
                >
                  <option
                    v-for="site in getSites"
                    :key="site.value"
                    :value="site.value"
                  >
                    {{ site.text }}
                  </option>
                </select>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">주 연락처</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.phone1"
                  v-maska="['###-###-####', '###-####-####']"
                  placeholder="주 연락처"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                보조 연락처
              </CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.phone2"
                  v-maska="['###-###-####', '###-####-####']"
                  placeholder="보조 연락처"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">주소</CFormLabel>
              <CCol sm="3">
                <CInputGroup>
                  <CInputGroupText @click="postCode.initiate()">
                    우편번호
                  </CInputGroupText>
                  <CFormInput
                    v-model="form.zipcode"
                    v-maska="'#####'"
                    placeholder="우편번호"
                    maxlength="5"
                    @focus="postCode.initiate()"
                  />
                  <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>
                </CInputGroup>
              </CCol>
              <CCol sm="7">
                <CFormInput
                  v-model="form.address1"
                  v-maska="'#####'"
                  placeholder="메인 주소"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label"></CFormLabel>
              <CCol sm="5">
                <CFormInput
                  ref="address2"
                  v-model="form.address2"
                  v-maska="'#####'"
                  placeholder="상세 주소"
                />
              </CCol>
              <CCol sm="5">
                <CFormInput
                  v-model="form.address3"
                  v-maska="'#####'"
                  placeholder="나머지 주소"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">
                주요 상담 기록
              </CFormLabel>
              <CCol sm="10">
                <CFormTextarea
                  v-model="form.counsel_record"
                  rows="4"
                  placeholder="주요 상담 기록"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </div>
    </CModalBody>

    <CModalFooter>
      <CButton type="button" color="light" @click="$emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          type="submit"
          :color="owner ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="owner"
          type="button"
          color="danger"
          @click="deleteConfirm"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>

    <DaumPostcode ref="postCode" @address-callback="addressCallback" />
  </CForm>

  <ConfirmModal ref="delModal">
    <template #header>
      <CIcon name="cilWarning" />
      사업 부지 정보 삭제
    </template>
    <template #default>
      삭제한 데이터는 복구할 수 없습니다. 해당 사업 부지 정보를
      삭제하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
