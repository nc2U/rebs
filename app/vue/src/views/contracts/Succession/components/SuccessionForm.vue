<script lang="ts" setup>
import { reactive, ref, watch, onBeforeMount, computed } from 'vue'
import { write_contract } from '@/utils/pageAuth'
import { isValidate } from '@/utils/helper'
import { dateFormat } from '@/utils/baseMixins'
import { maska as vMaska } from 'maska'
import { AddressData, callAddress } from '@/components/DaumPostcode/address'
import DaumPostcode from '@/components/DaumPostcode/index.vue'
import DatePicker from '@/components/DatePicker/index.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  succession: { type: Object, default: null },
  contractor: { type: Object, default: null },
})

const emit = defineEmits(['on-submit', 'close'])

const sameAddr = ref(false)
const address21 = ref()
const address22 = ref()
const alertModal = ref()
const confirmModal = ref()

const validated = ref(false)
const form = reactive({
  pk: undefined,
  apply_date: '',
  trading_date: '',
  is_approval: false,
  approval_date: null as string | null,
  note: '',
})

const contract = reactive({
  pk: undefined,
  serial_number: '',
})

const seller = reactive({
  pk: undefined,
  name: '',
})

const buyer = reactive({
  pk: undefined,
  name: '',
  birth_date: '',
  gender: 'M' as 'M' | 'F',
  id_zipcode: '',
  id_address1: '',
  id_address2: '',
  id_address3: '',
  dm_zipcode: '',
  dm_address1: '',
  dm_address2: '',
  dm_address3: '',
  cell_phone: '',
  home_phone: '',
  other_phone: '',
  email: '',
})

const formsCheck = computed(() => {
  if (props.succession) {
    const a = contract.pk === props.succession.contract.pk
    const b = contract.serial_number === props.succession.contract.serial_number
    const c = seller.pk === props.succession.seller.pk
    const d = seller.name === props.succession.seller.name
    const e = form.apply_date === props.succession.apply_date
    const f = form.trading_date === props.succession.trading_date
    const g = form.is_approval === props.succession.is_approval
    const h = form.approval_date === props.succession.approval_date
    const i = form.note === props.succession.note
    const j = buyer.name === props.succession.buyer.name
    const k = buyer.birth_date === props.succession.buyer.birth_date
    const l = buyer.gender === props.succession.buyer.gender
    const m = buyer.id_zipcode === props.succession.buyer.id_zipcode
    const n = buyer.id_address1 === props.succession.buyer.id_address1
    const o = buyer.id_address2 === props.succession.buyer.id_address2
    const p = buyer.id_address3 === props.succession.buyer.id_address3
    const q = buyer.dm_zipcode === props.succession.buyer.dm_zipcode
    const r = buyer.dm_address1 === props.succession.buyer.dm_address1
    const s = buyer.dm_address2 === props.succession.buyer.dm_address2
    const t = buyer.dm_address3 === props.succession.buyer.dm_address3
    const u = buyer.cell_phone === props.succession.buyer.cell_phone
    const v = buyer.home_phone === props.succession.buyer.home_phone
    const w = buyer.other_phone === props.succession.buyer.other_phone
    const x = buyer.email === props.succession.buyer.email
    const fc = a && b && c && d && e && f && g
    const bc = h && i && j && k && l && m && n && o && p && q && r
    const cc = s && t && u && v && w && x
    return fc && bc && cc
  } else return false
})

watch(form, val => {
  if (val.apply_date) form.apply_date = dateFormat(val.apply_date)
  if (val.trading_date) form.trading_date = dateFormat(val.trading_date)
  if (val.approval_date) form.approval_date = dateFormat(val.approval_date)
})

watch(buyer, val => {
  if (val.birth_date) buyer.birth_date = dateFormat(val.birth_date)
})

const onSubmit = (event: Event) => {
  if (write_contract.value) {
    if (isValidate(event)) {
      validated.value = true
    } else {
      const cData = { ...contract }
      const sData = { ...seller }
      const bData = { ...buyer }
      emit('on-submit', {
        ...form,
        ...{ contract: cData, seller: sData, buyer: bData },
      })
    }
  } else alertModal.value.callModal()
}

const deleteConfirm = () => {
  if (write_contract.value) confirmModal.value.callModal()
  else alertModal.value.callModal()
}

const modalAction = () => alert('this is ready!')

const addressCallback = (data: AddressData) => {
  const { formNum, zipcode, address1, address3 } = callAddress(data)
  if (formNum === 2) {
    buyer.id_zipcode = zipcode
    buyer.id_address1 = address1
    buyer.id_address2 = ''
    buyer.id_address3 = address3
    address21.value.$el.nextElementSibling.focus()
  } else if (formNum === 3) {
    buyer.dm_zipcode = zipcode
    buyer.dm_address1 = address1
    buyer.dm_address2 = ''
    buyer.dm_address3 = address3
    address22.value.$el.nextElementSibling.focus()
  }
}

const toSame = () => {
  if (!sameAddr.value) {
    buyer.dm_zipcode = buyer.id_zipcode
    buyer.dm_address1 = buyer.id_address1
    buyer.dm_address2 = buyer.id_address2
    buyer.dm_address3 = buyer.id_address3
  } else {
    buyer.dm_zipcode = ''
    buyer.dm_address1 = ''
    buyer.dm_address2 = ''
    buyer.dm_address3 = ''
  }
}

onBeforeMount(() => {
  contract.pk = props.contractor.contract
  seller.pk = props.contractor.pk
  seller.name = props.contractor.name
  if (props.succession) {
    form.pk = props.succession.pk
    form.apply_date = props.succession.apply_date
    form.trading_date = props.succession.trading_date
    form.is_approval = props.succession.is_approval
    form.approval_date = props.succession.approval_date
    form.note = props.succession.note

    buyer.pk = props.succession.buyer.pk
    buyer.name = props.succession.buyer.name
    buyer.birth_date = props.succession.buyer.birth_date
    buyer.gender = props.succession.buyer.gender
    buyer.id_zipcode = props.succession.buyer.id_zipcode
    buyer.id_address1 = props.succession.buyer.id_address1
    buyer.id_address2 = props.succession.buyer.id_address2
    buyer.id_address3 = props.succession.buyer.id_address3
    buyer.dm_zipcode = props.succession.buyer.dm_zipcode
    buyer.dm_address1 = props.succession.buyer.dm_address1
    buyer.dm_address2 = props.succession.buyer.dm_address2
    buyer.dm_address3 = props.succession.buyer.dm_address3
    buyer.cell_phone = props.succession.buyer.cell_phone
    buyer.home_phone = props.succession.buyer.home_phone
    buyer.other_phone = props.succession.buyer.other_phone
    buyer.email = props.succession.buyer.email
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
      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">양도계약자</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="seller.pk" required readonly>
                <option :value="contractor.pk">
                  {{ contractor.name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">계약건</CFormLabel>
            <CCol sm="8" class="text-left">
              <CFormSelect v-model="contract.pk" required readonly>
                <option :value="contractor.contract">
                  {{ contractor.__str__ }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              승계신청일
            </CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="form.apply_date"
                required
                placeholder="승계신청일"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              매매계약일
            </CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="form.trading_date"
                required
                placeholder="매매계약일"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <hr />
      <h6 class="pb-2">◼︎ 양수계약자 인적사항</h6>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">양수계약자</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="buyer.name"
                required
                placeholder="양수계약자 성명"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">생년월일</CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="buyer.birth_date"
                required
                placeholder="생년월일"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">성별</CFormLabel>
            <CCol sm="8" class="pt-2">
              <div class="form-check form-check-inline">
                <input
                  id="male"
                  v-model="buyer.gender"
                  class="form-check-input"
                  type="radio"
                  value="M"
                  name="gender"
                />
                <label class="form-check-label" for="male">남성</label>
              </div>
              <div class="form-check form-check-inline">
                <input
                  id="female"
                  v-model="buyer.gender"
                  class="form-check-input"
                  type="radio"
                  value="F"
                  name="gender"
                />
                <label class="form-check-label" for="female">여성</label>
              </div>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">휴대전화</CFormLabel>
            <CCol sm="8">
              <input
                v-model="buyer.cell_phone"
                v-maska="['###-###-####', '###-####-####']"
                class="form-control"
                maxlength="13"
                required
                placeholder="휴대전화"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">집전화</CFormLabel>
            <CCol sm="8">
              <input
                v-model="buyer.home_phone"
                v-maska="['###-###-####', '###-####-####']"
                class="form-control"
                maxlength="13"
                placeholder="집전화"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">기타연락처</CFormLabel>
            <CCol sm="8">
              <input
                v-model="buyer.other_phone"
                v-maska="['###-###-####', '###-####-####']"
                class="form-control"
                maxlength="13"
                placeholder="기타연락처"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">이메일</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="buyer.email"
                type="email"
                placeholder="이메일"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol>
          <CRow class="mb-2">
            <CFormLabel class="col-sm-2 col-form-label">
              주민등록주소
            </CFormLabel>
            <CCol xs="4">
              <CInputGroup>
                <CInputGroupText @click="$refs.postCode.initiate(2)">
                  우편번호
                </CInputGroupText>
                <CFormInput
                  v-model="buyer.id_zipcode"
                  v-maska="'#####'"
                  maxlength="5"
                  placeholder="우편번호"
                  required
                  @focus="$refs.postCode.initiate(2)"
                />
              </CInputGroup>
            </CCol>
            <CCol xs="6">
              <CFormInput
                v-model="buyer.id_address1"
                maxlength="35"
                placeholder="주민등록 메인 주소"
                required
                @focus="$refs.postCode.initiate(2)"
              />
            </CCol>
          </CRow>
          <CRow>
            <CCol xs="2" />
            <CCol xs="4">
              <CFormInput
                ref="address21"
                v-model="buyer.id_address2"
                maxlength="20"
                placeholder="상세주소(지번, 동호수)"
              />
            </CCol>
            <CCol xs="6">
              <CFormInput
                v-model="buyer.id_address3"
                maxlength="20"
                placeholder="참고항목(동, 건물)"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol>
          <CRow class="mb-2">
            <CFormLabel class="col-sm-2 col-form-label">
              우편송달주소
            </CFormLabel>
            <CCol xs="4">
              <CInputGroup>
                <CInputGroupText @click="$refs.postCode.initiate(3)">
                  우편번호
                </CInputGroupText>
                <CFormInput
                  v-model="buyer.dm_zipcode"
                  v-maska="'#####'"
                  maxlength="5"
                  placeholder="우편번호"
                  required
                  @focus="$refs.postCode.initiate(3)"
                />
              </CInputGroup>
            </CCol>
            <CCol xs="6">
              <CFormInput
                v-model="buyer.dm_address1"
                maxlength="35"
                placeholder="우편송달 메인 주소"
                required
                @focus="$refs.postCode.initiate(3)"
              />
            </CCol>
          </CRow>
          <CRow>
            <CCol xs="2" />
            <CCol xs="4">
              <CFormInput
                ref="address22"
                v-model="buyer.dm_address2"
                maxlength="20"
                placeholder="상세주소(지번, 동호수)"
              />
            </CCol>
            <CCol xs="6">
              <CInputGroup>
                <CFormInput
                  v-model="buyer.dm_address3"
                  maxlength="20"
                  placeholder="참고항목(동, 건물)"
                />
                <CInputGroupText>
                  <CFormCheck
                    id="toSame"
                    v-model="sameAddr"
                    label="상동"
                    @click="toSame"
                  />
                </CInputGroupText>
              </CInputGroup>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <hr />

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              변경인가여부
            </CFormLabel>
            <CCol sm="8" class="pt-2">
              <CFormSwitch
                id="isApproval"
                v-model="form.is_approval"
                label="변경인가완료"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              변경인가일
            </CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="form.approval_date"
                placeholder="변경인가일"
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
      <CButton type="button" color="light" @click="emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          type="submit"
          :color="succession ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="succession"
          type="button"
          color="danger"
          @click="deleteConfirm"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>
  </CForm>

  <DaumPostcode ref="postCode" @addressCallback="addressCallback" />

  <ConfirmModal ref="confirmModal">
    <template #header> 계약 해지 정보 - [삭제]</template>
    <template #default>
      삭제 후 복구할 수 없습니다. 해당 건별 수납 정보 삭제를 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
