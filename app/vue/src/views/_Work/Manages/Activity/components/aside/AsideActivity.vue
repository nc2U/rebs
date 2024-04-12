<script lang="ts" setup>
import { ref } from 'vue'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'

defineProps({
  hasSubs: { type: Boolean, default: false },
})

const form = ref({
  upToDate: dateFormat(new Date()),
  user: null as number | null,
  issue: true,
  changeSet: true,
  news: true,
  docs: true,
  file: true,
  wiki: false,
  message: false,
  spentTime: false,
  subProjects: true,
})
</script>

<template>
  <CRow class="mb-3">
    <CCol><h6 class="asideTitle">작업내역</h6></CCol>
  </CRow>
  <CRow class="mb-3">
    <CFormLabel for="log-date" class="col-sm-4 col-form-label">10일 기록</CFormLabel>
    <CCol>
      <DatePicker v-model="form.upToDate" id="log-date" />
    </CCol>
  </CRow>

  <CRow class="mb-3">
    <CFormLabel for="log-user" class="col-sm-4 col-form-label">사용자</CFormLabel>
    <CCol>
      <CFormSelect v-model="form.user" id="log-user" size="sm">
        <option>---------</option>
        <option>austin1</option>
        <option>austin2</option>
      </CFormSelect>
    </CCol>
  </CRow>

  <CRow class="mb-3">
    <CCol>
      <CFormCheck v-model="form.issue" label="업무" id="issue-filter" />
      <CFormCheck v-model="form.changeSet" label="변경묶음" id="changeset-filter" />
      <CFormCheck v-model="form.news" label="공지" id="news-filter" />
      <CFormCheck v-model="form.docs" label="문서" id="docs-filter" />
      <CFormCheck v-model="form.file" label="파일" id="file-filter" />
      <CFormCheck v-model="form.wiki" label="위키 편집" id="wiki-filter" />
      <CFormCheck v-model="form.message" label="글" id="message-filter" />
      <CFormCheck v-model="form.spentTime" label="작업시간" id="spent-time-filter" />
    </CCol>
  </CRow>

  <CRow v-if="hasSubs" class="mb-3">
    <CCol>
      <CFormCheck v-model="form.subProjects" label="하위 프로젝트" id="sub-project-filter" />
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CButton color="dark" size="sm">적용</CButton>
    </CCol>
  </CRow>
</template>

<style lang="scss" scoped>
.asideTitle {
  font-size: 1.1em;
}
</style>
