<script lang="ts" setup>
import { ref, onBeforeMount, type PropType, computed } from 'vue'
import type { Issue, IssueProject } from '@/store/types/work'
import { isValidate } from '@/utils/helper'
import DatePicker from '@/components/DatePicker/index.vue'
import MdEditor from '@/components/MdEditor/Index.vue'

const props = defineProps({
  iProject: { type: Object as PropType<IssueProject>, default: null },
  issue: { type: Object as PropType<Issue>, default: null },
  issueProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
})

const validated = ref(false)
const editDetails = ref(true)

const form = ref({
  pk: null as number | null,
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

const timeEntry = ref({
  issue: null as number | null,
  spent_on: '',
  hours: null as number | null,
  activity: null as number | null,
  comment: '',
})

const emit = defineEmits(['on-submit', 'close-form'])

const formCheck = computed(() => {
  if (props.issue) {
    const a = form.value.project === props.issue.project.slug
    const b = form.value.is_private === props.issue.is_private
    const c = form.value.tracker === props.issue.tracker
    const d = form.value.subject === props.issue.subject
    const e = form.value.description === props.issue.description
    const f = form.value.status === props.issue.status
    const g = form.value.parent === props.issue.parent
    const h = form.value.priority === props.issue.priority
    const i = form.value.start_date === props.issue.start_date
    const j = form.value.assigned_to === props.issue.assigned_to?.pk
    const k = form.value.due_date === props.issue.due_date
    const l = form.value.estimated_hours === props.issue.estimated_hours
    const m = form.value.done_ratio === props.issue.done_ratio
    return a && b && c && d && e && f && g && h && i && j && k && l && m
  } else return false
})

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    const e = form.value.estimated_hours

    if (form.value.estimated_hours) emit('on-submit', form.value)
  }
}

const closeForm = () => emit('close-form')

onBeforeMount(() => {
  if (props.iProject) form.value.project = props.iProject.slug
  if (props.issue) {
    editDetails.value = false

    form.value.pk = props.issue.pk
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
        <div v-if="issue">
          <h6>속성 변경</h6>
          <v-divider class="mt-0" />
        </div>
        <CRow class="mb-3">
          <CFormLabel for="project" class="col-sm-2 col-form-label text-right required">
            프로젝트
          </CFormLabel>

          <CCol sm="4">
            <CFormSelect v-model="form.project">
              <option v-for="proj in issueProjects" :value="proj.slug" :key="proj.slug">
                <span v-if="proj.depth === 2"> &nbsp;&nbsp;» </span>
                <span v-if="proj.depth === 3"> &nbsp;&nbsp;&nbsp;&nbsp;» </span>
                <span v-if="proj.depth === 4"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;» </span>
                <span v-if="proj.depth === 5">
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;»
                </span>
                {{ proj.name }}
              </option>
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
            <CFormSelect v-model="form.tracker" id="tracker" required>
              <option>기능</option>
            </CFormSelect>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="subject" class="col-sm-2 col-form-label text-right required">
            제목
          </CFormLabel>
          <CCol sm="10">
            <CFormInput v-model="form.subject" maxlength="100" id="subject" required />
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

          <CCol v-else sm="10" id="description">
            <MdEditor v-model="form.description" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="status" class="col-sm-2 col-form-label text-right required">
            상태
          </CFormLabel>
          <CCol sm="4">
            <CFormSelect v-model="form.status" id="status" required>
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
            <CFormSelect v-model="form.priority" id="priority" required>
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
          <div class="col-sm-3">
            <input
              v-model="form.estimated_hours"
              id="estimated_hours"
              maxlength="10"
              type="text"
              class="form-control"
            />
          </div>
          <div class="col-sm-1" style="padding-top: 6px">시간</div>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6"></CCol>

          <CFormLabel for="done_ratio" class="col-sm-2 col-form-label text-right">
            진척도
          </CFormLabel>
          <CCol sm="4">
            <CFormSelect v-model.number="form.done_ratio" id="done_ratio">
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
            <CFormLabel for="hours" class="col-sm-2 col-form-label text-right">
              소요시간
            </CFormLabel>
            <div class="col-sm-3">
              <!--              <CFormInput v-model.number="timeEntry.hours" type="number" min="0" id="hours" />-->
              <input
                v-model="timeEntry.hours"
                id="hours"
                maxlength="10"
                type="text"
                class="form-control"
              />
            </div>
            <div class="col-sm-1" style="padding-top: 6px">시간</div>

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

    <CButton type="submit" :color="issue ? 'success' : 'primary'" :disabled="formCheck">
      확인
    </CButton>
    <CButton type="button" color="light" @click="closeForm">취소</CButton>
  </CForm>
</template>