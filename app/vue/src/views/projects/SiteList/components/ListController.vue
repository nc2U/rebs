<script lang="ts" setup>
import { computed, reactive, nextTick } from 'vue'
import { useSite } from '@/store/pinia/project_site'
import { numFormat } from '@/utils/baseMixins'
import { bgLight } from '@/utils/cssMixins'

defineProps({ project: { type: Number, default: null } })
const emit = defineEmits(['list-filtering'])

const form = reactive({ search: '' })

const siteStore = useSite()

const siteCount = computed(() => siteStore.siteCount)

const formsCheck = computed(() => form.search.trim() === '')

const listFiltering = (page = 1) => {
  nextTick(() => {
    emit('list-filtering', { page, search: form.search.trim() })
  })
}

defineExpose({ listFiltering })

const resetForm = () => {
  form.search = ''
  listFiltering(1)
}
</script>

<template>
  <CCallout color="info" class="pb-0 mb-3" :class="bgLight">
    <CRow>
      <CCol lg="4" md="6">
        <CRow>
          <CCol class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="행정동, 지번, 소유자, 지목 검색"
                aria-label="search"
                :disabled="!project"
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
        <strong> 필지 건수 조회 결과 : {{ numFormat(siteCount) }} 건 </strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm"> 검색조건 초기화 </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
