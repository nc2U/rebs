<script lang="ts" setup>
import { computed, reactive, nextTick } from 'vue'
import { useSite } from '@/store/pinia/project_site'

const emit = defineEmits(['list-filtering'])

const form = reactive({
  search: '',
})

const siteStore = useSite()

const siteCount = computed(() => siteStore.siteCount)

const formsCheck = computed(() => form.search === '')

const listFiltering = (page = 1) => {
  nextTick(() => {
    emit('list-filtering', { page, search: form.search })
  })
}

defineExpose({ listFiltering })

const resetForm = () => {
  form.search = ''
  listFiltering(1)
}
</script>

<template>
  <CCallout color="secondary" class="pb-0 mb-3">
    <CRow>
      <CCol lg="8"></CCol>

      <CCol lg="4">
        <CRow>
          <CCol class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="행정동, 지번, 소유자, 지목 검색"
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
        <strong> 필지 건수 조회 결과 : {{ numFormat(siteCount) }} 건 </strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
