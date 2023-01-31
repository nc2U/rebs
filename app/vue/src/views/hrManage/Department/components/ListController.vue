<script lang="ts" setup="">
import { reactive, computed, nextTick } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import { useCompany } from '@/store/pinia/company'

const emit = defineEmits(['list-filtering'])

const form = reactive({
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

const listFiltering = (page = 1) => {
  nextTick(() => {
    emit('list-filtering', {
      page,
      dep: form.dep,
      rank: form.rank,
      sts: form.sts,
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
            <CFormSelect v-model="form.dep" @change="listFiltering(1)">
              <option value="">---------</option>
            </CFormSelect>
          </CCol>
          <CCol md="4" class="pb-0 mb-3">
            <CFormSelect v-model="form.rank" @change="listFiltering(1)">
              <option value="">---------</option>
            </CFormSelect>
          </CCol>
          <CCol md="4" class="pb-0 mb-3">
            <CFormSelect v-model="form.sts" @change="listFiltering(1)">
              <option value="">---------</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol md="6">
        <CRow class="justify-content-end">
          <CCol md="5" class="mb-3">
            <CInputGroup>
              <CFormInput
                v-model="form.q"
                placeholder="부서명 검색"
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
        <strong> 부서 수 조회 결과 : {{ numFormat(staffsCount) }} 건 </strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
