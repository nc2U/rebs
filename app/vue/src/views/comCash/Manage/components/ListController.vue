<script lang="ts" setup>
import { computed, reactive, watch, nextTick, onBeforeMount } from 'vue'
import { useComCash, DataFilter } from '@/store/pinia/comCash'
import { numFormat, dateFormat } from '@/utils/baseMixins'
import { maska as vMaska } from 'maska'
import DatePicker from '@/components/DatePicker/index.vue'

const emit = defineEmits(['list-filtering'])

const form = reactive<DataFilter>({
  page: 1,
  company: null,
  from_date: '',
  to_date: '',
  sort: '',
  account_d1: '',
  account_d2: '',
  account_d3: '',
  bank_account: '',
  search: '',
})

onBeforeMount(() => {
  //
})

const formsCheck = computed(() => {
  const a = form.from_date === ''
  const b = form.to_date === ''
  const c = form.sort === ''
  const d = form.account_d1 === ''
  const e = form.account_d2 === ''
  const f = form.account_d3 === ''
  const g = form.bank_account === ''
  const h = form.search === ''
  return a && b && c && d && e && f && g && h
})

const useComCashStore = useComCash()
const formAccD1List = computed(() => useComCashStore.formAccD1List)
const formAccD2List = computed(() => useComCashStore.formAccD2List)
const formAccD3List = computed(() => useComCashStore.formAccD3List)
const comBankList = computed(() => useComCashStore.comBankList)
const cashBookCount = computed(() => useComCashStore.cashBookCount)

watch(form, val => {
  if (val.from_date) {
    form.from_date = dateFormat(val.from_date)
    listFiltering(1)
  }
  if (val.to_date) {
    form.to_date = dateFormat(val.to_date)
    listFiltering(1)
  }
})

//   methods: {
const sortSelect = () => {
  listFiltering(1)
  form.account_d1 = ''
  form.account_d2 = ''
  form.account_d3 = ''
}
const accountD1Select = () => {
  listFiltering(1)
  form.account_d2 = ''
  form.account_d3 = ''
}
const accountD2Select = () => {
  listFiltering(1)
  form.account_d3 = ''
}

const listFiltering = (page = 1) => {
  form.page = page
  nextTick(() => {
    emit('list-filtering', { ...form })
  })
}

defineExpose({ listFiltering })

const resetForm = () => {
  form.from_date = ''
  form.to_date = ''
  form.sort = ''
  form.account_d1 = ''
  form.account_d2 = ''
  form.account_d3 = ''
  form.bank_account = ''
  form.search = ''
  listFiltering(1)
}
</script>

<template>
  <CCallout color="primary" class="pb-0 mb-4">
    <CRow>
      <CCol lg="3">
        <CRow>
          <CCol md="6" class="mb-3">
            <DatePicker
              v-model="form.from_date"
              v-maska="'####-##-##'"
              placeholder="시작일 (From)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>
          <CCol md="6" class="mb-3">
            <DatePicker
              v-model="form.to_date"
              v-maska="'####-##-##'"
              placeholder="종료일 (To)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="5">
        <CRow>
          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.sort" @change="sortSelect">
              <option value="">구분</option>
              <option value="1">입금</option>
              <option value="2">출금</option>
              <option value="3">대체</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.account_d1" @change="accountD1Select">
              <option value="">계정[대분류]</option>
              <option
                v-for="acc1 in formAccD1List"
                :key="acc1.pk"
                :value="acc1.pk"
              >
                {{ acc1.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect
              v-model="form.account_d2"
              :disabled="!form.account_d1"
              @change="accountD2Select"
            >
              <option value="">계정[중분류]</option>
              <option
                v-for="acc2 in formAccD2List"
                :key="acc2.pk"
                :value="acc2.pk"
              >
                {{ acc2.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect
              v-model="form.account_d3"
              :disabled="!form.account_d1"
              @change="listFiltering(1)"
            >
              <option value="">계정[소분류]</option>
              <option
                v-for="acc3 in formAccD3List"
                :key="acc3.pk"
                :value="acc3.pk"
              >
                {{ acc3.name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="4">
        <CRow>
          <CCol md="6" lg="4" class="mb-3">
            <CFormSelect v-model="form.bank_account" @change="listFiltering(1)">
              <option value="">거래계좌</option>
              <option v-for="acc in comBankList" :key="acc.pk" :value="acc.pk">
                {{ acc.alias_name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="8" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="적요, 거래처 검색"
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
        <strong>
          거래 건수 조회 결과 : {{ numFormat(cashBookCount) }} 건
        </strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
