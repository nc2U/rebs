<script lang="ts" setup>
import {ref, reactive, computed, watch, onBeforeMount} from 'vue'
import {useSite} from '@/store/pinia/project_site'
import {dateFormat} from '@/utils/baseMixins'
import {isValidate} from '@/utils/helper'
import {SiteContract} from '@/store/types/project'
import {write_project} from '@/utils/pageAuth'
import Multiselect from '@vueform/multiselect'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  project: {type: Number, default: null},
  contract: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const validated = ref(false)

const form = reactive<SiteContract>({
  pk: null,
  project: null,
  owner: null,
  contract_date: null,
  total_price: null,
  contract_area: null,
  down_pay1: null,
  down_pay1_is_paid: false,
  down_pay2: null,
  down_pay2_is_paid: false,
  inter_pay1: null,
  inter_pay1_date: null as string | null,
  inter_pay1_is_paid: false,
  inter_pay2: null,
  inter_pay2_date: null as string | null,
  inter_pay2_is_paid: false,
  remain_pay: null,
  remain_pay_date: null,
  remain_pay_is_paid: false,
  ownership_completion: false,
  acc_bank: '',
  acc_number: '',
  acc_owner: '',
  note: '',
})

const siteStore = useSite()
const getOwners = computed(() => siteStore.getOwners)

const formsCheck = computed(() => {
  if (props.contract) {
    const a = form.owner === props.contract.owner
    const b = form.contract_date === props.contract.contract_date
    const c = form.total_price === props.contract.total_price
    const d = form.contract_area === props.contract.contract_area
    const e = form.down_pay1 === props.contract.down_pay1
    const f = form.down_pay1_is_paid === props.contract.down_pay1_is_paid
    const g = form.down_pay2 === props.contract.down_pay2
    const h = form.down_pay2_is_paid === props.contract.down_pay2_is_paid
    const i = form.inter_pay1 === props.contract.inter_pay1
    const j = form.inter_pay1_date === props.contract.inter_pay1_date
    const k = form.inter_pay1_is_paid === props.contract.inter_pay1_is_paid
    const l = form.inter_pay2 === props.contract.inter_pay2
    const m = form.inter_pay2_date === props.contract.inter_pay2_date
    const n = form.inter_pay2_is_paid === props.contract.inter_pay2_is_paid
    const o = form.remain_pay === props.contract.remain_pay
    const p = form.remain_pay_date === props.contract.remain_pay_date
    const q = form.remain_pay_is_paid === props.contract.remain_pay_is_paid
    const r = form.ownership_completion === props.contract.ownership_completion
    const s = form.acc_bank === props.contract.acc_bank
    const t = form.acc_number === props.contract.acc_number
    const u = form.acc_owner === props.contract.acc_owner
    const v = form.note === props.contract.note

    const sky = a && b && c && d && e && f && g && h && i
    const sea = j && k && l && m && n && o && p && q && r
    const air = s && t && u && v

    return sky && sea && air
  } else return false
})

const getAreaByOwner = computed(() =>
    !props.contract && siteStore.siteOwner
        ? siteStore.siteOwner.sites
            .map(s => Number(s.owned_area))
            .reduce((sum, val) => sum + val, 0)
        : null,
)

watch(form, val => {
  if (val.contract_date) form.contract_date = dateFormat(val.contract_date)
  if (val.inter_pay1_date)
    form.inter_pay1_date = dateFormat(val.inter_pay1_date)
  if (val.inter_pay2_date)
    form.inter_pay2_date = dateFormat(val.inter_pay2_date)
  if (val.remain_pay_date)
    form.remain_pay_date = dateFormat(val.remain_pay_date)
  if (!props.contract && val.owner) siteStore.fetchSiteOwner(val.owner)
})

watch(getAreaByOwner, val => (form.contract_area = val))

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    if (write_project) multiSubmit({...form})
    else alertModal.value.callModal()
  }
}

const multiSubmit = (multiPayload: SiteContract) => {
  emit('multi-submit', multiPayload)
  emit('close')
}

const deleteObject = () => {
  emit('on-delete', {pk: props.contract.pk, project: props.contract.project})
  delModal.value.close()
  emit('close')
}

const deleteConfirm = () => {
  if (write_project) delModal.value.callModal()
  else alertModal.value.callModal()
}

onBeforeMount(() => {
  if (props.contract) {
    form.pk = props.contract.pk
    form.project = props.contract.project
    form.owner = props.contract.owner
    form.contract_date = props.contract.contract_date
    form.total_price = props.contract.total_price
    form.contract_area = props.contract.contract_area
    form.down_pay1 = props.contract.down_pay1
    form.down_pay1_is_paid = props.contract.down_pay1_is_paid
    form.down_pay2 = props.contract.down_pay2
    form.down_pay2_is_paid = props.contract.down_pay2_is_paid
    form.inter_pay1 = props.contract.inter_pay1
    form.inter_pay1_date = props.contract.inter_pay1_date
    form.inter_pay1_is_paid = props.contract.inter_pay1_is_paid
    form.inter_pay2 = props.contract.inter_pay2
    form.inter_pay2_date = props.contract.inter_pay2_date
    form.inter_pay2_is_paid = props.contract.inter_pay2_is_paid
    form.remain_pay = props.contract.remain_pay
    form.remain_pay_date = props.contract.remain_pay_date
    form.remain_pay_is_paid = props.contract.remain_pay_is_paid
    form.ownership_completion = props.contract.ownership_completion
    form.acc_bank = props.contract.acc_bank
    form.acc_number = props.contract.acc_number
    form.acc_owner = props.contract.acc_owner
    form.note = props.contract.note
  } else form.project = props.project
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
              <CFormLabel class="col-sm-4 col-form-label">소유자</CFormLabel>
              <CCol sm="8">
                <Multiselect
                    v-model.number="form.owner"
                    :options="getOwners"
                    placeholder="소유자"
                    autocomplete="label"
                    :attrs="form.owner ? {} : { required: true }"
                    :classes="{ search: 'form-control multiselect-search' }"
                    :add-option-on="['enter' | 'tab']"
                    searchable
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                총 계약면적
              </CFormLabel>
              <CCol sm="8">
                <CFormInput
                    v-model.number="form.contract_area"
                    type="number"
                    min="0"
                    step="0.0000001"
                    placeholder="총 계약면적"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                총 매매가격
              </CFormLabel>
              <CCol sm="8">
                <CFormInput
                    v-model.number="form.total_price"
                    min="0"
                    type="number"
                    required
                    placeholder="총 매매가격"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계약 체결일
              </CFormLabel>
              <CCol sm="8">
                <DatePicker
                    v-model="form.contract_date"
                    maxlength="10"
                    placeholder="계약 체결일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계약금 (1차)
              </CFormLabel>
              <CCol sm="8">
                <CInputGroup class="mb-3">
                  <CFormInput
                      v-model.number="form.down_pay1"
                      type="number"
                      min="0"
                      placeholder="계약금 - 1차"
                  />
                  <CInputGroupText>
                    <CFormCheck
                        id="down_pay1_is_paid"
                        v-model="form.down_pay1_is_paid"
                        type="checkbox"
                        label="지급"
                    />
                  </CInputGroupText>
                </CInputGroup>
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계약금 (2차)
              </CFormLabel>
              <CCol sm="8">
                <CInputGroup class="mb-3">
                  <CFormInput
                      v-model.number="form.down_pay2"
                      type="number"
                      min="0"
                      placeholder="계약금 - 2차"
                  />
                  <CInputGroupText>
                    <CFormCheck
                        id="down_pay2_is_paid"
                        v-model="form.down_pay2_is_paid"
                        type="checkbox"
                        label="지급"
                    />
                  </CInputGroupText>
                </CInputGroup>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                중도금 (1차)
              </CFormLabel>
              <CCol sm="8">
                <CInputGroup class="mb-3">
                  <CFormInput
                      v-model.number="form.inter_pay1"
                      type="number"
                      min="0"
                      placeholder="중도금 - 1차"
                  />
                  <CInputGroupText>
                    <CFormCheck
                        id="inter_pay1_is_paid"
                        v-model="form.inter_pay1_is_paid"
                        type="checkbox"
                        label="지급"
                    />
                  </CInputGroupText>
                </CInputGroup>
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                지급 일자
              </CFormLabel>
              <CCol sm="8">
                <DatePicker
                    v-model="form.inter_pay1_date"
                    :required="false"
                    maxlength="10"
                    placeholder="중도금 1차 지급일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                중도금 (2차)
              </CFormLabel>
              <CCol sm="8">
                <CInputGroup class="mb-3">
                  <CFormInput
                      v-model.number="form.inter_pay2"
                      type="number"
                      min="0"
                      placeholder="중도금 - 2차"
                  />
                  <CInputGroupText>
                    <CFormCheck
                        id="inter_pay2_is_paid"
                        v-model="form.inter_pay2_is_paid"
                        type="checkbox"
                        label="지급"
                    />
                  </CInputGroupText>
                </CInputGroup>
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                지급 일자
              </CFormLabel>
              <CCol sm="8">
                <DatePicker
                    v-model="form.inter_pay2_date"
                    :required="false"
                    maxlength="10"
                    placeholder="중도금 2차 지급일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">계약 잔금</CFormLabel>
              <CCol sm="8">
                <CInputGroup class="mb-3">
                  <CFormInput
                      v-model.number="form.remain_pay"
                      type="number"
                      min="0"
                      required
                      placeholder="계약 잔금"
                  />
                  <CInputGroupText>
                    <CFormCheck
                        id="remain_pay_is_paid"
                        v-model="form.remain_pay_is_paid"
                        type="checkbox"
                        label="지급"
                    />
                  </CInputGroupText>
                </CInputGroup>
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                지급 일자
              </CFormLabel>
              <CCol sm="8">
                <DatePicker
                    v-model="form.remain_pay_date"
                    :required="false"
                    maxlength="10"
                    placeholder="잔금 지급일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">
                입금 은행
              </CFormLabel>
              <CCol sm="3">
                <CFormInput
                    v-model="form.acc_bank"
                    maxlength="20"
                    required
                    placeholder="입금 은행"
                />
              </CCol>
              <CCol sm="3">
                <CFormInput
                    v-model="form.acc_number"
                    maxlength="25"
                    required
                    placeholder="계좌번호"
                />
              </CCol>
              <CCol sm="2">
                <CFormInput
                    v-model="form.acc_owner"
                    maxlength="20"
                    required
                    placeholder="예금주"
                />
              </CCol>
              <CCol sm="2" class="pt-2">
                <CFormSwitch
                    id="ownership_completion"
                    v-model="form.ownership_completion"
                    label="소유권 확보"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">
                특이사항
              </CFormLabel>
              <CCol sm="10">
                <CFormTextarea
                    v-model="form.note"
                    rows="3"
                    placeholder="특이사항"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </div>
    </CModalBody>

    <CModalFooter>
      <CButton type="button" color="light" @click="emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
            type="submit"
            :color="contract ? 'success' : 'primary'"
            :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
            v-if="contract"
            type="button"
            color="danger"
            @click="deleteConfirm"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>
  </CForm>

  <ConfirmModal ref="delModal">
    <template #header>
      <CIcon name="cilWarning"/>
      부지 매입 계약 정보 삭제
    </template>
    <template #default>
      삭제한 데이터는 복구할 수 없습니다. 해당 부지 매입 계약 정보를
      삭제하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal"/>
</template>
