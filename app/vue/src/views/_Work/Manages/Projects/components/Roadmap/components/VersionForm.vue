<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import { isValidate } from '@/utils/helper'
import { colorLight } from '@/utils/cssMixins'
import DatePicker from '@/components/DatePicker/index.vue'

const emit = defineEmits(['aside-visible', 'on-submit'])

const validated = ref(false)

const form = ref({
  pk: null as number | null,
  project: '',
  name: '',
  description: '',
  wiki_page_title: '',
  effective_date: null as string | null,
  sharing: '0' as '0' | '1' | '2' | '3' | '4',
  is_default: false,
})

const route = useRoute()

const workStore = useWork()
const version = computed(() => workStore.version)

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    const is_back = !!route.query.back
    emit('on-submit', { ...form.value }, is_back)
  }
}

const setupForm = () => {
  if (version.value) {
    form.value.pk = version.value.pk as number
    form.value.project = version.value.project as string
    form.value.name = version.value.name
    form.value.description = version.value.description
    form.value.wiki_page_title = version.value.wiki_page_title
    form.value.effective_date = version.value.effective_date
    form.value.sharing = version.value.sharing
    form.value.is_default = !!version.value.is_default
  }
}

const resetForm = () => {
  form.value.pk = null
  form.value.project = ''
  form.value.name = ''
  form.value.description = ''
  form.value.wiki_page_title = ''
  form.value.effective_date = null
  form.value.sharing = '0'
  form.value.is_default = false
}

onBeforeMount(async () => {
  emit('aside-visible', false)

  if (route.params.verId) {
    await workStore.fetchVersion(Number(route.params.verId))
    setupForm()
  } else resetForm()
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5><span v-if="route.name === '(로드맵) - 추가'">새</span> 버전</h5>
    </CCol>

    <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="onSubmit">
      <CCard :color="colorLight" class="mb-2">
        <CCardBody>
          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right required">
              이름
            </CFormLabel>

            <CCol sm="10" lg="6">
              <CFormInput v-model="form.name" required />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right"> 설명</CFormLabel>

            <CCol sm="10" lg="6">
              <CFormInput v-model="form.description" />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right">
              위키 페이지
            </CFormLabel>

            <CCol sm="10" lg="6">
              <CFormInput v-model="form.wiki_page_title" />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right"> 날짜</CFormLabel>

            <CCol sm="6">
              <DatePicker v-model="form.effective_date" />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right"> 공유</CFormLabel>

            <CCol sm="6">
              <CFormSelect v-model="form.sharing">
                <option value="0">공유 없음</option>
                <option value="1">하위 프로젝트</option>
                <option value="2">상위 및 하위 프로젝트</option>
                <option value="3">최상위 및 모든 하위 프로젝트</option>
                <option value="4">모든 프로젝트</option>
              </CFormSelect>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right">
              기본 버전
            </CFormLabel>

            <CCol sm="6" class="pt-2">
              <CFormCheck v-model="form.is_default" />
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>

      <CButton type="submit" color="primary"> 저장</CButton>
    </CForm>
  </CRow>
</template>
