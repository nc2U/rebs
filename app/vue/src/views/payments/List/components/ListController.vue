<script lang="ts" setup>
import { computed, reactive, ref, nextTick, watch } from 'vue'
import { usePayment } from '@/store/pinia/payment'
import { useProCash } from '@/store/pinia/proCash'
import { dateFormat } from '@/utils/baseMixins'
import { maska as vMaska } from 'maska'
import DatePicker from '@/components/DatePicker/index.vue'

const emit = defineEmits(['payment-filtering'])

const from_date = ref('')
const to_date = ref('')

const form = reactive({
  pay_order: '',
  pay_account: '',
  no_contract: false,
  search: '',
})

const paymentStore = usePayment()
const payOrderList = computed(() => paymentStore.payOrderList)
const paymentsCount = computed(() => paymentStore.paymentsCount)

const proCashStore = useProCash()
const proBankAccountList = computed(() => proCashStore.proBankAccountList)

const formsCheck = computed(() => {
  const a = !from_date.value
  const b = !to_date.value
  const c = !form.pay_order
  const d = !form.pay_account
  const e = !form.no_contract
  const f = form.search.trim() === ''
  return a && b && c && d && e && f
})

watch(from_date, val => {
  if (val) from_date.value = dateFormat(val)
  listFiltering(1)
})
watch(to_date, val => {
  if (val) to_date.value = dateFormat(val)
  listFiltering(1)
})

const listFiltering = (page = 1) => {
  nextTick(() => {
    form.search = form.search.trim()
    emit('payment-filtering', {
      ...{ page, from_date: from_date.value, to_date: to_date.value },
      ...form,
    })
  })
}
defineExpose({ listFiltering })

const resetForm = () => {
  from_date.value = ''
  to_date.value = ''
  form.pay_order = ''
  form.pay_account = ''
  form.no_contract = false
  form.search = ''
  listFiltering(1)
}
</script>

<template>
  <CCallout color="warning" class="pb-0 mb-4">
    <CRow>
      <CCol lg="7">
        <CRow>
          <CCol md="6" lg="3" class="mb-3">
            <DatePicker
              v-model="from_date"
              v-maska="'####-##-##'"
              placeholder="납부일자 (From)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <DatePicker
              v-model="to_date"
              v-maska="'####-##-##'"
              placeholder="납부일자 (To)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.pay_order" @change="listFiltering(1)">
              <option value="">납부회차 선택</option>
              <option v-for="po in payOrderList" :key="po.pk" :value="po.pk">
                {{ po.__str__ }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.pay_account" @change="listFiltering(1)">
              <option value="">납부계좌 선택</option>
              <option
                v-for="ba in proBankAccountList"
                :key="ba.pk"
                :value="ba.pk"
              >
                {{ ba.alias_name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
      <CCol lg="5">
        <CRow>
          <CCol md="6" class="mb-3 pl-4 pt-2">
            <CFormSwitch
              id="no_contract"
              v-model="form.no_contract"
              label="미등록 납부대금 건"
              @change="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="계약자, 입금자, 적요, 비고"
                aria-label="Username"
                aria-describedby="addon-wrapping"
                @keydown.enter="listFiltering(1)"
              />
              <CInputGroupText @click="listFiltering(1)">검색</CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <CRow>
      <CCol color="warning" class="p-2 pl-3">
        <strong>납부 건수 조회 결과 : {{ paymentsCount }} 건</strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
