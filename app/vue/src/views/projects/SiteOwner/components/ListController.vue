<script lang="ts" setup>
import { computed, reactive, nextTick } from 'vue'
import { useSite } from '@/store/pinia/project_site'

const emit = defineEmits(['list-filtering'])

const form = reactive({
  own_sort: '',
  search: '',
})

const own_sort_select = [
  { val: '1', text: '개인' },
  { val: '2', text: '법인' },
  { val: '3', text: '국공유지' },
]

const siteStore = useSite()
const siteOwnerCount = computed(() => siteStore.siteOwnerCount)

const formsCheck = computed(() => form.own_sort === '' && form.search === '')

const listFiltering = (page = 1) => {
  nextTick(() => {
    emit('list-filtering', {
      page,
      own_sort: form.own_sort,
      search: form.search,
    })
  })
}

defineExpose({ listFiltering })

const resetForm = () => {
  form.own_sort = ''
  form.search = ''
  listFiltering(1)
}
</script>

<template>
  <CCallout color="success" class="pb-0 mb-3">
    <CRow>
      <CCol lg="4" md="6">
        <CRow>
          <CCol md="4" class="mb-3">
            <CFormSelect v-model="form.own_sort" @change="listFiltering">
              <option value="">소유구분</option>
              <option
                v-for="sort in own_sort_select"
                :key="sort.val"
                :value="sort.val"
              >
                {{ sort.text }}
              </option>
            </CFormSelect>
          </CCol>
          <CCol class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="소유자, 연락처, 지번, 상담기록 검색"
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
        <strong>
          소유자 수 조회 결과 : {{ numFormat(siteOwnerCount) }} 건
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
