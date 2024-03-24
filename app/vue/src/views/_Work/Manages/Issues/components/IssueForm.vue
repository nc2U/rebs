<script lang="ts" setup>
import { ref, onBeforeMount, type PropType } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import MdEditor from '@/components/MdEditor/Index.vue'
import type { Issue } from '@/store/types/work'

const props = defineProps({
  issue: {
    type: Object as PropType<Issue>,
    default: null,
  },
})

const validated = ref(false)
const editDetails = ref(true)
const form = ref({
  project: '',
  is_private: false,
  tracker: '',
  subject: '',
  description: '',
  status: '신규',
  parent: null as number | null,
  priority: '보통',
  start_date: null as string | null,
  assigned_to: null as number | null,
  due_date: null as string | null,
  estimated_hours: null as number | null,
  done_ratio: 0,
  watchers: [] as number[],
})

const emit = defineEmits(['on-submit', 'close-form'])

const onSubmit = () => {
  emit('on-submit', form.value)
}

const closeForm = () => emit('close-form')

onBeforeMount(() => {
  if (props.issue) {
    editDetails.value = false

    form.value.project = props.issue.project.slug
    form.value.is_private = props.issue.is_private
    form.value.tracker = props.issue.tracker
    form.value.subject = props.issue.subject
    form.value.description = props.issue.description
    form.value.status = props.issue.status
    form.value.parent = props.issue.parent
    form.value.priority = props.issue.priority
    form.value.start_date = props.issue.start_date
    form.value.assigned_to = props.issue.assigned_to?.pk ?? null
    form.value.due_date = props.issue.due_date
    form.value.estimated_hours = props.issue.estimated_hours
    form.value.done_ratio = props.issue.done_ratio
  }
})
</script>

<template>
  <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="onSubmit">
    <CCard color="light" class="mb-2">
      <CCardBody>
        <h6>속성 변경</h6>
        <v-divider class="mt-0" />
        <CRow class="mb-3">
          <CFormLabel for="project" class="col-sm-2 col-form-label text-right required">
            프로젝트
          </CFormLabel>
          <CCol sm="4">
            <CFormSelect v-model="form.project" id="project">
              <option value="redmine">redmine</option>
            </CFormSelect>
          </CCol>
          <CCol style="padding-top: 8px">
            <CFormCheck v-model="form.is_private" id="is_private" label="비공개" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="tracker" class="col-sm-2 col-form-label text-right required">
            유형
          </CFormLabel>
          <CCol sm="4">
            <CFormSelect v-model="form.tracker" id="tracker">
              <option>기능</option>
            </CFormSelect>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="subject" class="col-sm-2 col-form-label text-right required">
            제목
          </CFormLabel>
          <CCol sm="10">
            <CFormInput v-model="form.subject" id="subject" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="description" class="col-sm-2 col-form-label text-right">
            설명
          </CFormLabel>
          <CCol v-if="!editDetails" sm="10" style="padding-top: 6px">
            <v-icon icon="mdi-pencil" size="sm" color="amber" />
            <router-link to="" @click="() => (editDetails = true)">편집</router-link>
          </CCol>
          <CCol v-else sm="10">
            <MdEditor v-model="form.description" id="description" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="status" class="col-sm-2 col-form-label text-right required">
            상태
          </CFormLabel>
          <CCol sm="4">
            <CFormSelect v-model="form.status" id="status">
              <option>진행</option>
            </CFormSelect>
          </CCol>

          <CFormLabel for="parent" class="col-sm-2 col-form-label text-right">
            상위 업무
          </CFormLabel>
          <CCol sm="4">
            <CFormSelect v-model="form.parent" id="parent">
              <option value=""></option>
            </CFormSelect>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="priority" class="col-sm-2 col-form-label text-right required">
            우선순위
          </CFormLabel>
          <CCol sm="4">
            <CFormSelect v-model="form.priority" id="priority">
              <option>보통</option>
            </CFormSelect>
          </CCol>

          <CFormLabel for="start_date" class="col-sm-2 col-form-label text-right">
            시작일
          </CFormLabel>
          <CCol sm="4">
            <DatePicker v-model="form.start_date" id="start_date" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="assigned_to" class="col-sm-2 col-form-label text-right">
            담당자
          </CFormLabel>
          <CCol sm="4">
            <CFormSelect v-model="form.assigned_to" id="assigned_to">
              <option value="1">admin</option>
            </CFormSelect>
          </CCol>

          <CFormLabel for="due_date" class="col-sm-2 col-form-label text-right">
            완료일
          </CFormLabel>
          <CCol sm="4">
            <DatePicker v-model="form.due_date" id="due_date" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6"></CCol>

          <CFormLabel for="estimated_hours" class="col-sm-2 col-form-label text-right">
            추정시간
          </CFormLabel>
          <CCol sm="4">
            <CInputGroup>
              <CFormInput v-model="form.estimated_hours" id="estimated_hours" placeholder="시간" />
              <CInputGroupText>시간</CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6"></CCol>

          <CFormLabel for="done_ratio" class="col-sm-2 col-form-label text-right">
            진척도
          </CFormLabel>
          <CCol sm="4">
            <CFormSelect v-model="form.done_ratio" id="done_ratio">
              <option :value="0">0%</option>
              <option :value="10">10%</option>
              <option :value="20">20%</option>
              <option :value="30">30%</option>
              <option :value="40">40%</option>
              <option :value="50">50%</option>
              <option :value="60">60%</option>
              <option :value="70">70%</option>
              <option :value="80">80%</option>
              <option :value="90">90%</option>
              <option :value="100">100%</option>
            </CFormSelect>
          </CCol>
        </CRow>

        <div v-if="!issue">
          <CRow class="mb-3">
            <CFormLabel for="file" class="col-sm-2 col-form-label text-right"> 파일</CFormLabel>
            <CCol sm="4">
              <CFormInput id="file" type="file" />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="watcher" class="col-sm-2 col-form-label text-right">
              업무 열람 공유자
            </CFormLabel>
            <CCol sm="4" style="padding-top: 8px">
              <CFormCheck v-model="form.watchers" id="watcher" label="austin kho" />
            </CCol>
          </CRow>
        </div>

        <div v-else>
          <h6>작업시간 기록</h6>
          <v-divider class="mt-0" />
          <CRow class="mb-3">
            <CFormLabel for="issue-project" class="col-sm-2 col-form-label text-right">
              소요시간
            </CFormLabel>
            <CCol sm="4">
              <CInputGroup>
                <CFormInput
                  v-model="form.estimated_hours"
                  id="estimated_hours"
                  placeholder="시간"
                />
                <CInputGroupText>시간</CInputGroupText>
              </CInputGroup>
            </CCol>

            <CFormLabel for="issue-project" class="col-sm-2 col-form-label text-right">
              작업종류
            </CFormLabel>
            <CCol sm="4">
              <CFormSelect>
                <option value="">---------</option>
              </CFormSelect>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="issue-project" class="col-sm-2 col-form-label text-right">
              설명
            </CFormLabel>
            <CCol sm="10">
              <CFormInput />
            </CCol>
          </CRow>

          <h6>댓글</h6>
          <v-divider class="mt-0" />
          <MdEditor style="height: 180px" />
        </div>
      </CCardBody>
    </CCard>

    <CButton type="button" color="light" @click="closeForm" size="sm">취소</CButton>
  </CForm>
</template>
