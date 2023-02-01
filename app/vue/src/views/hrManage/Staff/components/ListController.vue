<script lang="ts" setup="">
import { reactive, computed, nextTick } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import { useCompany } from '@/store/pinia/company'
import Multiselect from '@vueform/multiselect'

const emit = defineEmits(['list-filtering'])

const form = reactive({
  page: 1,
  com: 1,
  dep: '',
  rank: '',
  sts: '',
  q: '',
})

const formsCheck = computed(
  () =>
    form.dep === '' &&
    form.rank === '' &&
    form.sts === '' &&
    form.q.trim() === '',
)

const comStore = useCompany()
const staffsCount = computed(() => comStore.staffsCount)
const getPkDeparts = computed(() => comStore.getPkDeparts)
const getPkRanks = computed(() => comStore.getPkRanks)

const getStatus = [
  { value: '1', label: '근무 중' },
  { value: '2', label: '휴직 중' },
  { value: '3', label: '퇴직신청' },
  { value: '4', label: '퇴사처리' },
]

const listFiltering = (page = 1) => {
  nextTick(() => {
    emit('list-filtering', {
      page,
      dep: form.dep || '',
      rank: form.rank || '',
      sts: form.sts || '',
      q: form.q.trim(),
    })
  })
}

const resetForm = () => {
  form.dep = ''
  form.rank = ''
  form.sts = ''
  form.q = ''
  listFiltering(1)
}

defineExpose({ listFiltering })
</script>

<template>
  <CCallout class="pb-0 mb-3">
    <CRow>
      <CCol md="6">
        <CRow>
          <CCol md="4" class="mb-3">
            <Multiselect
              v-model.number="form.dep"
              :options="getPkDeparts"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
              placeholder="부서별"
              @change="listFiltering(1)"
            />
          </CCol>
          <CCol md="4" class="pb-0 mb-3">
            <Multiselect
              v-model.number="form.rank"
              :options="getPkRanks"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
              placeholder="직급별"
              @change="listFiltering(1)"
            />
          </CCol>
          <CCol md="4" class="pb-0 mb-3">
            <Multiselect
              v-model.number="form.sts"
              :options="getStatus"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
              placeholder="상태별"
              @change="listFiltering(1)"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol md="6">
        <CRow class="justify-content-end">
          <CCol md="5" class="mb-3">
            <CInputGroup>
              <CFormInput
                v-model="form.q"
                placeholder="직원 성명, 이메일 검색"
                aria-label="search"
                @keydown.enter="listFiltering(1)"
              />
              <CInputGroupText @click="listFiltering(1)">검색</CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <CRow>
      <CCol class="p-2 pl-3">
        <strong> 직원 수 조회 결과 : {{ numFormat(staffsCount) }} 건 </strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
