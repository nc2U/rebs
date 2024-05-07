<script lang="ts" setup>
import { ref, onBeforeMount, type PropType, computed, watch, inject, type ComputedRef } from 'vue'
import type { CodeValue, Issue, IssueFile, IssueProject, IssueStatus } from '@/store/types/work'
import type { User } from '@/store/types/accounts'
import { isValidate } from '@/utils/helper'
import { useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import { colorLight } from '@/utils/cssMixins'
import Multiselect from '@vueform/multiselect'
import MdEditor from '@/components/MdEditor/Index.vue'
import DatePicker from '@/components/DatePicker/index.vue'
import WatcherAdd from '@/views/_Work/Manages/Issues/components/aside/WatcherAdd.vue'

const props = defineProps({
  issueProject: { type: Object as PropType<IssueProject>, default: null },
  issue: { type: Object as PropType<Issue>, default: null },
  allProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
  statusList: { type: Array as PropType<IssueStatus[]>, default: () => [] },
  activityList: { type: Array as PropType<CodeValue[]>, default: () => [] },
  priorityList: { type: Array as PropType<CodeValue[]>, default: () => [] },
  getIssues: { type: Array as PropType<{ value: number; label: string }[]>, default: () => [] },
})

const emit = defineEmits(['on-submit', 'close-form'])

const refWatcherAdd = ref()

const validated = ref(false)
const editDetails = ref(true)

const form = ref({
  pk: null as number | null,
  project: '',
  is_private: false,
  tracker: null as number | null,
  subject: '',
  description: '',
  status: 1 as number | null,
  parent: null as number | null,
  priority: 2 as number | null,
  start_date: null as string | null,
  assigned_to: null as number | null,
  due_date: null as string | null,
  estimated_hours: null as number | string | null,
  done_ratio: 0,
  watchers: [] as number[],
  files: [] as IssueFile[],
})

const statuses = computed(() =>
  props.issue ? props.statusList : props.statusList.filter(s => s.pk === 1),
)

const assignedToMe = () => (form.value.assigned_to = userInfo?.value.pk as number)

const timeEntry = ref({
  issue: null as number | null,
  spent_on: '',
  hours: null as number | string | null,
  activity: null as number | null,
  comment: '',
})

const comment = ref({
  content: '',
  is_private: false,
})

const fileEdit = ref(false)
const newFiles = ref<{ file: File; description: string }[]>([])

const loadFile = (data: Event) => {
  const el = data.target as HTMLInputElement
  if (el.files && el.files[0]) newFiles.value.push({ file: el.files[0], description: '' })
}

const removeFile = (n: number) => {
  if (n - 1 === 0) {
    const file_form = document.getElementById(`file-${n}`) as HTMLInputElement
    file_form.value = ''
  } else {
    const file_row = document.getElementById(`row-fn-${n}`)
    file_row?.parentNode?.removeChild(file_row)
  }
  newFiles.value.splice(n - 1, 1)
}

const formCheck = computed(() => {
  if (props.issue) {
    const a = form.value.project === props.issue.project.slug
    const b = form.value.is_private === props.issue.is_private
    const c = form.value.tracker === props.issue.tracker.pk
    const d = form.value.subject === props.issue.subject
    const e = form.value.description === props.issue.description
    const f = form.value.status === props.issue.status.pk
    const g = form.value.parent === props.issue.parent
    const h = form.value.priority === props.issue.priority.pk
    const i = form.value.start_date === props.issue.start_date
    const j = form.value.assigned_to === props.issue.assigned_to?.pk
    const k = form.value.due_date === props.issue.due_date
    const l = form.value.estimated_hours === numToTime(props.issue.estimated_hours)
    const m = form.value.done_ratio === props.issue.done_ratio
    const n = !form.value.files?.map(f => f.del).some(f => f === true)
    const o = !newFiles.value.length
    const p = !timeEntry.value.hours
    const q = !timeEntry.value.activity
    const r = !timeEntry.value.comment
    const s = !comment.value.content

    const first = a && b && c && d && e && f && g && h && i
    const second = j && k && l && m && n && o && p && q && r && s
    return first && second
  } else return false
})

const route = useRoute()
const workStore = useWork()
watch(props, nVal => {
  if (nVal.issueProject) form.value.project = nVal?.issueProject.slug
})

const watcherList = ref<{ pk: number; username: string }[]>([])

const memberList = computed(() =>
  (props.issueProject ? props.issueProject.all_members : workStore.memberList)?.map(m => m.user),
)

watch(
  () => memberList.value,
  nVal => (watcherList.value = nVal ?? []),
)

const trackerList = computed(() =>
  props.issueProject ? props.issueProject.trackers : workStore.trackerList,
)

const watcherAddSubmit = (payload: { pk: number; username: string }[]) => {
  form.value.watchers = [...new Set([...form.value.watchers, ...payload.map(p => p.pk)])]
  payload.forEach(p => {
    if (!watcherList.value.map(w => w.pk).includes(p.pk))
      watcherList.value.push({ pk: p.pk, username: p.username })
  })
}

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    let noSubmit = false
    if (!!timeEntry.value.hours) {
      const time_entry_hours = timeToNum(timeEntry.value.hours, false)
      if (time_entry_hours) timeEntry.value.hours = time_entry_hours
      else noSubmit = true
    }

    if (!!form.value.estimated_hours) {
      const estimated_hours = timeToNum(form.value.estimated_hours, true)
      if (estimated_hours) form.value.estimated_hours = estimated_hours
      else noSubmit = true
    }

    if (noSubmit) return
    else {
      emit('on-submit', {
        ...form.value,
        ...timeEntry.value,
        newFiles: newFiles.value,
        comment_content: comment.value.content,
      })
      validated.value = false
    }
  }
}

const removeProperty = (e: Event) => {
  const el = e.currentTarget as HTMLInputElement
  el.removeAttribute('required')
}

const closeForm = () => emit('close-form')

const userInfo = inject<ComputedRef<User>>('userInfo')

const callComment = (edit?: true) => {
  // 댓글 폼 불러오기
  comment.value.content = edit
    ? ''
    : userInfo?.value.username +
      '의 댓글: \n' +
      form.value.description
        .split('\n')
        .map(line => ` > ${line}`)
        .join('  \n') +
      '\n\n'
}

defineExpose({ callComment })

const numToTime = (n: number | null) => {
  if (!n) return ''
  else {
    const hours = Math.floor(n)
    const minutes = Math.round((n - hours) * 60)
    const str = minutes >= 10 ? '' : '0'
    return `${hours}:${str}${minutes}`
  }
}

const timeToNum = (n: number | string | null, estimated: boolean) => {
  const timeNum = Number(n)

  if (!!timeNum) {
    return Math.floor(timeNum) < 1000 ? n : 999.99
  } else {
    const regex = /^(0|[1-9]\d*):(0[0-9]|[1-5][0-9])$/
    const timeStr = String(n)

    if (regex.test(timeStr)) {
      const time = timeStr.split(':')
      return (
        (Number(time[0]) < 999 ? Number(time[0]) : 999) + Number((Number(time[1]) / 60).toFixed(2))
      )
    } else {
      validated.value = true
      if (estimated) {
        form.value.estimated_hours = ''
        document.getElementById('estimated_hours')?.setAttribute('required', 'true')
        return null
      } else {
        timeEntry.value.hours = ''
        document.getElementById('hours')?.setAttribute('required', 'true')
        return null
      }
    }
  }
}

onBeforeMount(() => {
  watcherList.value = memberList.value ?? []
  if (props.issue) {
    editDetails.value = false

    form.value.pk = props.issue.pk
    form.value.project = props.issue.project.slug
    form.value.is_private = props.issue.is_private
    form.value.tracker = props.issue.tracker.pk
    form.value.subject = props.issue.subject
    form.value.description = props.issue.description
    form.value.status = props.issue.status.pk
    form.value.parent = props.issue.parent
    form.value.priority = props.issue.priority.pk
    form.value.start_date = props.issue.start_date
    form.value.assigned_to = props.issue.assigned_to?.pk ?? null
    form.value.due_date = props.issue.due_date
    form.value.estimated_hours = numToTime(props.issue.estimated_hours)
    form.value.done_ratio = props.issue.done_ratio
    form.value.files = props.issue.files
    workStore.fetchIssueList({ status__closed: '', project: props.issue.project.slug })
  }
  if (route.params.projId) form.value.project = route.params.projId as string
  if (route.query.tracker) form.value.tracker = Number(route.query.tracker)
  if (route.query.parent) form.value.parent = Number(route.query.parent)
})
</script>

<template>
  <CRow class="py-2">
    <CCol id="edit-form">
      <h5>
        {{ !issue ? '새 업무만들기' : '편집' }}
      </h5>
    </CCol>

    <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="onSubmit">
      <CCard :color="colorLight" class="mb-2">
        <CCardBody>
          <div v-if="issue">
            <h6>속성 변경</h6>
            <v-divider class="mt-0" />
          </div>
          <CRow v-show="!route.query.parent" class="mb-3">
            <CFormLabel for="project" class="col-sm-2 col-form-label text-right required">
              프로젝트
            </CFormLabel>

            <CCol sm="4">
              <CFormSelect v-model="form.project" required>
                <option value="">---------</option>
                <option v-for="proj in allProjects" :value="proj.slug" :key="proj.slug">
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
              <CFormSelect v-model.number="form.tracker" id="tracker" required>
                <option value="">---------</option>
                <option v-for="tr in trackerList" :value="tr.pk" :key="tr.pk">
                  {{ tr.name }}
                </option>
              </CFormSelect>
            </CCol>
            <CCol v-if="form.tracker" class="pt-1">
              {{ trackerList.filter(t => t.pk === form.tracker).map(t => t.description)[0] }}
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
              <CFormSelect v-model.number="form.status" id="status" required>
                <option value="">---------</option>
                <option v-for="status in statuses" :value="status.pk" :key="status.pk">
                  {{ status.name }}
                </option>
              </CFormSelect>
            </CCol>

            <CFormLabel for="parent" class="col-sm-2 col-form-label text-right">
              상위 업무
            </CFormLabel>
            <CCol sm="4">
              <Multiselect
                v-model="form.parent"
                :options="getIssues"
                id="parent"
                placeholder="상위 업무 선택"
                :classes="{
                  search: 'form-control multiselect-search',
                  tagsSearch: 'form-control',
                }"
                searchable
              />
            </CCol>
          </CRow>

          <CRow v-show="!!issue && !issue.sub_issues.length" class="mb-3">
            <CFormLabel for="priority" class="col-sm-2 col-form-label text-right required">
              우선순위
            </CFormLabel>
            <CCol sm="4">
              <CFormSelect v-model.number="form.priority" id="priority" required>
                <option value="">---------</option>
                <option v-for="pr in priorityList" :value="pr.pk" :key="pr.pk">
                  {{ pr.name }}
                </option>
              </CFormSelect>
            </CCol>

            <CFormLabel for="start_date" class="col-sm-2 col-form-label text-right">
              시작일자
            </CFormLabel>
            <CCol sm="4">
              <DatePicker v-model="form.start_date" id="start_date" />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="assigned_to" class="col-sm-2 col-form-label text-right">
              담당자
            </CFormLabel>
            <div class="col-sm-3">
              <CFormSelect v-model.number="form.assigned_to" id="assigned_to">
                <option value="">---------</option>
                <option :value="userInfo?.pk">&lt;&lt; 나 &gt;&gt;</option>
                <option v-for="user in memberList" :value="user.pk" :key="user.pk">
                  {{ user.username }}
                </option>
              </CFormSelect>
            </div>
            <div class="col-sm-1" style="padding-top: 6px">
              <a
                v-if="form.assigned_to !== userInfo?.pk"
                href="javascript:void(0)"
                @click="assignedToMe"
              >
                나에게 할당
              </a>
            </div>

            <CFormLabel
              v-if="!!issue && !issue.sub_issues.length"
              for="due_date"
              class="col-sm-2 col-form-label text-right"
            >
              완료기한
            </CFormLabel>
            <CCol v-if="!!issue && !issue.sub_issues.length" sm="4">
              <DatePicker v-model="form.due_date" id="due_date" />
            </CCol>

            <CFormLabel v-else for="estimated_hours" class="col-sm-2 col-form-label text-right">
              추정시간
            </CFormLabel>
            <div v-if="!!issue && issue.sub_issues.length" class="col-sm-3">
              <CFormInput
                v-model="form.estimated_hours"
                id="estimated_hours"
                maxlength="6"
                type="text"
                class="form-control"
                @input="removeProperty"
                feedbackInvalid="999 이하의 정수, 실수 또는 '12:59' 과 같이 시간 형식을 입력하세요."
              />
            </div>
            <div
              v-if="!!issue && issue.sub_issues.length"
              class="col-sm-1"
              style="padding-top: 6px"
            >
              시간
            </div>
          </CRow>

          <CRow v-if="!!issue && !issue.sub_issues.length" class="mb-3">
            <CCol sm="6"></CCol>

            <CFormLabel for="estimated_hours" class="col-sm-2 col-form-label text-right">
              추정시간
            </CFormLabel>
            <div class="col-sm-3">
              <CFormInput
                v-model="form.estimated_hours"
                id="estimated_hours"
                maxlength="6"
                type="text"
                class="form-control"
                @input="removeProperty"
                feedbackInvalid="999 이하의 정수, 실수 또는 '12:59' 과 같이 시간 형식을 입력하세요."
              />
            </div>
            <div class="col-sm-1" style="padding-top: 6px">시간</div>
          </CRow>

          <CRow v-if="!!issue && !issue.sub_issues.length" class="mb-3">
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
            <div v-for="n in newFiles.length + 1" :key="n">
              <CRow :id="`row-fn-${n}`" class="mb-2">
                <CFormLabel :for="`file-${n}`" class="col-sm-2 col-form-label text-right">
                  <span v-if="n === 1">파일</span>
                </CFormLabel>
                <CCol sm="4">
                  <CFormInput :id="`file-${n}`" type="file" @change="loadFile" />
                </CCol>
                <CCol v-if="newFiles[n - 1]?.file" sm="6">
                  <CInputGroup>
                    <CFormInput v-model="newFiles[n - 1].description" placeholder="부가적인 설명" />
                    <CInputGroupText
                      v-if="newFiles.length === n"
                      @click="removeFile(n)"
                      :disabled="true"
                    >
                      <v-icon icon="mdi-trash-can-outline" size="16" />
                    </CInputGroupText>
                  </CInputGroup>
                </CCol>
              </CRow>
            </div>

            <CRow class="mb-3">
              <CFormLabel for="watcher" class="col-sm-2 col-form-label text-right">
                업무 관람자
              </CFormLabel>
              <CCol sm="10" style="padding-top: 8px">
                <span v-for="user in watcherList" :key="user.pk" class="mr-3">
                  <input
                    v-model="form.watchers"
                    :id="`user-${user.pk}`"
                    :value="user.pk"
                    type="checkbox"
                    class="form-check-input"
                  />
                  <label :for="`user-${user.pk}`" class="form-label form-check-label ml-2">
                    {{ user.username }}
                  </label>
                </span>
              </CCol>
              <CCol class="col-sm-2"></CCol>
              <CCol class="form-text">
                <v-icon icon="mdi-plus-circle" color="success" size="sm" class="mr-2" />
                <router-link to="" @click="refWatcherAdd.callModal()">
                  추가할 업무 관람자 검색
                </router-link>
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
                <CFormInput
                  v-model="timeEntry.hours"
                  maxlength="6"
                  id="hours"
                  @input="removeProperty"
                  feedbackInvalid="999 이하의 정수, 실수 또는 '12:59' 과 같이 시간 형식을 입력하세요."
                />
              </div>
              <div class="col-sm-1" style="padding-top: 6px">시간</div>

              <CFormLabel for="issue-project" class="col-sm-2 col-form-label text-right">
                작업종류
              </CFormLabel>
              <CCol sm="4">
                <CFormSelect v-model="timeEntry.activity" :required="!!timeEntry.hours">
                  <option value="">---------</option>
                  <option v-for="act in activityList" :value="act.pk" :key="act.pk">
                    {{ act.name }}
                  </option>
                </CFormSelect>
              </CCol>
            </CRow>

            <CRow class="mb-3">
              <CFormLabel for="issue-project" class="col-sm-2 col-form-label text-right">
                설명
              </CFormLabel>
              <CCol sm="10">
                <CFormInput v-model="timeEntry.comment" />
              </CCol>
            </CRow>

            <CRow class="mb-3">
              <CCol>
                <h6>댓글</h6>
                <v-divider class="mt-0" />
                <MdEditor v-model="comment.content" style="height: 180px" class="mb-1" />
                <CFormCheck v-model="comment.is_private" id="private_comment" label="비공개 댓글" />
              </CCol>
            </CRow>

            <CRow>
              <CCol>
                <h6>파일</h6>

                <CRow v-if="fileEdit" class="mb-2">
                  <CCol>
                    <CRow v-for="(file, i) in issue.files" :key="file.pk">
                      <CCol class="cursor-not-allowed col-sm-4">
                        <v-icon icon="mdi-paperclip" size="sm" color="grey" class="mr-2" />
                        <span :class="{ del: form.files[i].del }"> {{ file.file_name }} </span>
                      </CCol>

                      <CCol>
                        <CFormCheck
                          v-model="form.files[i].del"
                          :id="`file-del-${file.pk}`"
                          label="삭제"
                        />
                      </CCol>
                    </CRow>
                  </CCol>
                </CRow>

                <v-divider class="mt-0" />

                <div v-for="n in newFiles.length + 1" :key="n">
                  <CRow :id="`row-fn-${n}`" class="mb-2">
                    <CCol sm="4">
                      <CFormInput :id="`file-${n}`" type="file" @change="loadFile" />
                    </CCol>
                    <CCol v-if="newFiles[n - 1]?.file" sm="4">
                      <CInputGroup>
                        <CFormInput
                          v-model="newFiles[n - 1].description"
                          placeholder="부가적인 설명"
                        />
                        <CInputGroupText
                          v-if="newFiles.length === n"
                          @click="removeFile(n)"
                          :disabled="true"
                        >
                          <v-icon icon="mdi-trash-can-outline" size="16" />
                        </CInputGroupText>
                      </CInputGroup>
                    </CCol>
                    <CCol v-if="form.files?.length && n === 1" class="text-right">
                      <router-link to="" @click="fileEdit = !fileEdit">첨부파일 편집</router-link>
                    </CCol>
                  </CRow>
                </div>
              </CCol>
            </CRow>
          </div>
        </CCardBody>
      </CCard>

      <CButton type="submit" :color="issue ? 'success' : 'primary'" :disabled="formCheck">
        확인
      </CButton>
      <CButton type="button" color="light" @click="closeForm">취소</CButton>
    </CForm>
  </CRow>

  <WatcherAdd
    ref="refWatcherAdd"
    :watchers="issue?.watchers"
    @watcher-add-submit="watcherAddSubmit"
  />
</template>

<style lang="scss" scoped>
.del {
  color: #888;
  text-decoration: line-through;
}
</style>
