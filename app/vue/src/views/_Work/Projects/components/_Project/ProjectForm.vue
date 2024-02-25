<script lang="ts" setup="">
import { ref } from 'vue'
import QuillEditor from '@/components/QuillEditor/index.vue'

const validated = ref(false)

const form = ref({
  pk: undefined,
  name: '',
  desc: '',
  identifier: '',
  homepage: null,
  is_public: true,
  parent_project: null,
  is_inherit_members: false,
})

const module = ref({
  issue: true,
  time: true,
  news: true,
  document: true,
  file: true,
  wiki: true,
  repository: true,
  forum: true,
  calendar: true,
  gantt: true,
})

const onSubmit = () => 1
</script>

<template>
  <CRow>
    <CCol class="my-3">
      <h5>새 프로젝트</h5>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 생성'" class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '프로젝트 - 생성' }" class="ml-1">새 프로젝트</router-link>
      </span>
      <span>
        <v-icon icon="mdi-cog" color="secondary" size="sm" />
        <router-link :to="{ name: '프로젝트 목록' }" class="ml-1">관리</router-link>
      </span>
    </CCol>
  </CRow>

  <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="onSubmit">
    <CCard class="mb-3">
      <CCardBody>
        <CRow class="mb-3">
          <CFormLabel class="required col-form-label text-right col-2">이름</CFormLabel>
          <CCol>
            <CFormInput v-model="form.name" placeholder="프로젝트 이름" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">설명</CFormLabel>
          <CCol class="mb-5">
            <QuillEditor v-model="form.desc" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="required col-form-label text-right col-2">식별자</CFormLabel>
          <CCol>
            <CFormInput
              v-model="form.identifier"
              placeholder="프로젝트 식별자"
              text="1에서 100글자 소문자(a-z), 숫자, 대쉬(-)와 밑줄(_)만 가능합니다. 식별자 저장 후에는 수정할 수 없습니다."
            />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">홈페이지</CFormLabel>
          <CCol>
            <CFormInput v-model="form.homepage" placeholder="홈페이지 URL" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">공개여부</CFormLabel>
          <CCol class="pt-2">
            <CFormSwitch v-model="form.is_public" label="프로젝트 공개 여부" />
            <div class="form-text">
              공개 프로젝트는 네트워크의 모든 사용자가 접속할 수 있습니다.
            </div>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">상위 프로젝트</CFormLabel>
          <CCol>
            <CFormSelect v-model="form.parent_project">
              <option>----------</option>
            </CFormSelect>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">상위 프로젝트 구성원 상속</CFormLabel>
          <CCol class="pt-2">
            <CFormSwitch v-model="form.is_inherit_members" label="상위 프로젝트 구성원 상속 여부" />
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>

    <h6>
      <v-icon icon="mdi-check-bold" size="sm" color="success" />
      모듈
    </h6>
    <CCard class="mb-3">
      <CCardBody>
        <CRow>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.issue" id="issue" label="업무관리" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.time" id="time" label="시간추적" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.news" id="news" label="공지" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.document" id="document" label="문서" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.file" id="file" label="파일" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.wiki" id="wiki" label="위키" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.repository" id="repository" label="저장소" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.forum" id="forum" label="게시판" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.calendar" id="calendar" label="달력" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.gantt" id="gantt" label="Gantt 차트" />
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>

    <CRow>
      <CCol>
        <CButton color="primary">저장</CButton>
        <CButton color="primary">저장 후 계속하기</CButton>
      </CCol>
    </CRow>
  </CForm>
</template>
