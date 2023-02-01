<script lang="ts" setup="">
import { reactive, computed, nextTick } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import { useCompany } from '@/store/pinia/company'
import Multiselect from '@vueform/multiselect'

const emit = defineEmits(['list-filtering'])

const form = reactive({
  sort: '',
  q: '',
})

const formsCheck = computed(() => form.sort === '' && form.q.trim() === '')

const comStore = useCompany()
const ranksCount = computed(() => comStore.ranksCount)

const getSorts = [
  { value: '1', label: '임원' },
  { value: '2', label: '직원' },
]

const listFiltering = (page = 1) => {
  nextTick(() => {
    emit('list-filtering', {
      page,
      sort: form.sort || '',
      q: form.q.trim(),
    })
  })
}

const resetForm = () => {
  form.sort = ''
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
          <CCol md="4" class="pb-0 mb-3">
            <Multiselect
              v-model="form.sort"
              :options="getSorts"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
              placeholder="임/직원"
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
                placeholder="직급, 직함, 설명 검색"
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
        <strong> 직급 수 조회 결과 : {{ numFormat(ranksCount) }} 건 </strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
