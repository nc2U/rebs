<script lang="ts" setup>
import { computed, reactive, ref, watch, nextTick } from 'vue'
import { useStore } from 'vuex'
import { dateFormat } from '@/utils/baseMixins'
import { maska as vMaska } from 'maska'
import DatePicker from '@/components/DatePicker/index.vue'

const emit = defineEmits(['list-filtering'])

const from_date = ref('')
const to_date = ref('')
const form = reactive({
  sort: '',
  pro_acc_d1: '',
  pro_acc_d2: '',
  bank_account: '',
  search: '',
})

const store = useStore()

const sortList = computed(() => store.state.proCash.sortList)
const formAccD1List = computed(() => store.state.proCash.formAccD1List)
const formAccD2List = computed(() => store.state.proCash.formAccD2List)
const proImprestCount = computed(() => store.state.proCash.proImprestCount)
const imprestBAccount = computed(() => store.getters['proCash/imprestBAccount'])

const formsCheck = computed(() => {
  const a = from_date.value === ''
  const b = to_date.value === ''
  const c = form.sort === ''
  const d = form.pro_acc_d1 === ''
  const e = form.pro_acc_d2 === ''
  const f = form.bank_account === ''
  const g = form.search === ''
  return a && b && c && d && e && f && g
})

watch(from_date, () => listFiltering(1))
watch(to_date, () => listFiltering(1))

const pro_acc_d1Select = () => {
  listFiltering(1)
  form.pro_acc_d1 = ''
  form.pro_acc_d2 = ''
}

const pro_acc_d2Select = () => {
  listFiltering(1)
  form.pro_acc_d2 = ''
}

const listFiltering = (page = 1) => {
  nextTick(() => {
    const from = from_date.value ? dateFormat(from_date.value) : ''
    const to = to_date.value ? dateFormat(to_date.value) : ''
    emit('list-filtering', {
      ...{ page, from_date: from, to_date: to },
      ...form,
    })
  })
}
defineExpose({ listFiltering })

const resetForm = () => {
  from_date.value = ''
  to_date.value = ''
  form.sort = ''
  form.pro_acc_d1 = ''
  form.pro_acc_d2 = ''
  form.bank_account = ''
  form.search = ''
  listFiltering(1)
}
</script>

<template>
  <CCallout color="success" class="pb-0 mb-3">
    <CRow>
      <CCol lg="9">
        <CRow>
          <CCol md="6" lg="2" class="mb-3">
            <DatePicker
              v-model="from_date"
              v-maska="'####-##-##'"
              placeholder="시작일 (From)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <DatePicker
              v-model="to_date"
              v-maska="'####-##-##'"
              placeholder="종료일 (To)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.sort" @change="pro_acc_d1Select">
              <option value="">거래구분</option>
              <option v-for="sort in sortList" :key="sort.pk" :value="sort.pk">
                {{ sort.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.pro_acc_d1" @change="pro_acc_d2Select">
              <option value="">상위 항목</option>
              <option v-for="d1 in formAccD1List" :key="d1.pk" :value="d1.pk">
                {{ d1.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.pro_acc_d2" @change="listFiltering(1)">
              <option value="">하위 항목</option>
              <option v-for="d2 in formAccD2List" :key="d2.pk" :value="d2.pk">
                {{ d2.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.bank_account" @change="listFiltering(1)">
              <option value="">거래계좌</option>
              <option
                v-for="acc in imprestBAccount"
                :key="acc.pk"
                :value="acc.pk"
              >
                {{ acc.alias_name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="3">
        <CRow>
          <CCol class="mb-3">
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
          거래 건수 조회 결과 : {{ numFormat(proImprestCount) }} 건
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
