<script lang="ts" setup>
import { ref, computed, onBeforeMount, type PropType } from 'vue'
import { isValidate } from '@/utils/helper'
import { useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import DatePicker from '@/components/DatePicker/index.vue'
import Multiselect from '@vueform/multiselect'
import type { IssueProject } from '@/store/types/work'

const props = defineProps({
  timeEntry: { type: Object, default: null },
  issueProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
})

const validated = ref(false)

const form = ref({
  pk: null as number | null,
  project: null,
  issue: null,
  user: null,
  spent_on: '',
  hours: '',
  comment: '',
  activity: '',
})

const emit = defineEmits(['on-submit', 'close-form'])

const formCheck = computed(() => {
  if (props.timeEntry) {
    const a = form.value.project === props.timeEntry.project
    const b = form.value.issue === props.timeEntry.issue
    const c = form.value.spent_on === props.timeEntry.spent_on
    const d = form.value.hours === props.timeEntry.hours
    const e = form.value.comment === props.timeEntry.comment
    const f = form.value.activity === props.timeEntry.activity
    return a && b && c && d && e && f
  } else return false
})

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else emit('on-submit', { ...form.value })
}

const closeForm = () => emit('close-form')

const workStore = useWork()
const issueProject = computed(() => workStore.issueProject)
const activityList = computed(() => workStore.activityList)
const memberList = computed(() =>
  issueProject.value ? issueProject.value.all_members : workStore.memberList,
)
const getIssues = computed(() => workStore.getIssues)

const route = useRoute()

onBeforeMount(() => {
  if (issueProject.value) form.value.project = issueProject.value.slug
  if (props.timeEntry) {
    form.value.pk = props.timeEntry.pk
    form.value.issue = props.timeEntry.issue.pk
    form.value.user = props.timeEntry.user.pk
    form.value.spent_on = props.timeEntry.spent_on
    form.value.hours = props.timeEntry.hours
    form.value.comment = props.timeEntry.comment
    form.value.activity = props.timeEntry.activity
  }
  if (route.params.projId) {
    workStore.fetchIssueProject(route.params.projId as string)
    form.value.project = route.params.projId as string
  }
  workStore.fetchMemberList()
  workStore.fetchActivityList()
  workStore.fetchIssueList()
})
</script>

<template>
  <CCol>
    <h5>소요시간</h5>
  </CCol>

  {{ timeEntry }}

  <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="onSubmit">
    <CRow class="py-2">
      <CCard color="light" class="mb-2">
        <CCardBody>
          <CRow class="mb-3">
            <CFormLabel for="project" class="col-sm-2 col-form-label text-right required">
              프로젝트
            </CFormLabel>

            <CCol sm="4">
              <CFormSelect v-model="form.project" id="project" required>
                <option value="">---------</option>
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

            <CFormLabel for="issue" class="col-sm-2 col-form-label text-right required">
              업무
            </CFormLabel>
            <CCol sm="4">
              <Multiselect
                v-model="form.issue"
                :options="getIssues"
                id="issue"
                placeholder="업무 선택"
                :classes="{
                  search: 'form-control multiselect-search',
                  tagsSearch: 'form-control',
                }"
                searchable
                required
              />
            </CCol>
          </CRow>

          <CRow v-if="$route.name.includes('편집')" class="mb-3">
            <CFormLabel for="user" class="col-sm-2 col-form-label text-right required">
              사용자
            </CFormLabel>
            <CCol sm="4">
              <CFormSelect v-model="form.user" id="user" required>
                <option value="">---------</option>
                <option v-for="mem in memberList" :value="mem.user.pk" :key="mem.user.pk">
                  {{ mem.user.username }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="spent_on" class="col-sm-2 col-form-label text-right required">
              작업일자
            </CFormLabel>
            <CCol sm="4">
              <DatePicker v-model="form.spent_on" id="spent_on" required />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="hours" class="col-sm-2 col-form-label text-right required">
              시간
            </CFormLabel>
            <CCol sm="4">
              <CFormInput
                v-model="form.hours"
                id="hours"
                maxlength="10"
                placeholder="소요시간"
                required
              />
            </CCol>

            <CFormLabel for="activity" class="col-sm-2 col-form-label text-right required">
              작업종류
            </CFormLabel>
            <CCol sm="4">
              <CFormSelect v-model="form.activity" id="activity" required>
                <option value="">---------</option>
                <option v-for="act in activityList" :value="act.pk" :key="act.pk">
                  {{ act.name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="comment" class="col-sm-2 col-form-label text-right"> 설명</CFormLabel>
            <CCol sm="10">
              <CFormInput
                v-model="form.comment"
                id="comment"
                maxlength="255"
                placeholder="소요시간에 대한 메모"
              />
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>

      <CCol>
        <CButton type="submit" :color="timeEntry ? 'success' : 'primary'" :disabled="formCheck">
          확인
        </CButton>
        <CButton type="button" color="light" @click="closeForm">취소</CButton>
      </CCol>
    </CRow>
  </CForm>
</template>
