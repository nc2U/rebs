<script lang="ts" setup>
import { ref, reactive, type PropType, onBeforeMount, watch } from 'vue'
import type { IssueProject, IssueStatus, Tracker, TimeEntryFilter } from '@/store/types/work'
import { useRoute } from 'vue-router'
import DatePicker from '@/components/DatePicker/index.vue'
import Multiselect from '@vueform/multiselect'

const props = defineProps({
  allProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
  statusList: { type: Array as PropType<IssueStatus[]>, default: () => [] },
  trackerList: { type: Array as PropType<Tracker[]>, default: () => [] },
})

const emit = defineEmits(['filter-submit'])

const viewMode = ref<'board' | 'list'>('board')
const condVisible = ref(true)
const optVisible = ref(false)

const searchCond = ref(['work_date'])
const resetFilter = () => {
  searchCond.value = ['work_date']
  filterSubmit()
}

const searchOptions = reactive([
  {
    options: [
      { value: 'issue', label: '업무' },
      { value: 'user', label: '사용자' },
      { value: 'author', label: '저자', disabled: true },
      { value: 'activity', label: '작업종류', disabled: true },
      { value: 'hours', label: '시간', disabled: true },
      { value: 'work_date', label: '작업시간', disabled: true },
    ],
  },
  {
    label: '문자열 검색',
    options: [{ value: 'comment', label: '설명' }],
    disabled: true,
  },
  {
    label: '업무',
    options: [
      { value: 'tracker', label: '업무의 유형', disabled: true },
      { value: 'parent', label: '업무의 상위업무', disabled: true },
      { value: 'status', label: '업무의 상태', disabled: true },
      { value: 'target_version', label: '업무의 목표버전', disabled: true },
      { value: 'subject', label: '업무의 제목', disabled: true },
    ],
    disabled: true,
  },
  {
    label: '프로젝트',
    options: [{ value: 'project_status', label: '프로젝트의 상태', disabled: true }],
    disabled: true,
  },
])

const cond = ref({
  work_date: 'any' as
    | 'is'
    | '>='
    | '<='
    | 'between'
    | 'before_days'
    | 'today'
    | 'yesterday'
    | 'this_week'
    | 'last_week'
    | 'this_month'
    | 'last_month'
    | 'this_year'
    | 'none'
    | 'any',
  project: 'is' as 'is' | 'exclude',
  issue: 'is' as 'is' | 'keyword' | 'none' | 'any',
  user: 'is' as 'is' | 'exclude' | 'none' | 'any',
  author: 'is' as 'is' | 'exclude' | 'none' | 'any',
  activity: 'is' as 'is' | 'exclude',
  hours: 'is' as 'is' | '>=' | '<=' | 'between' | 'none' | 'any',

  comment: 'contain' as 'contain' | 'start_with' | 'end_with' | 'none' | 'any',

  issue_tracker: 'is' as 'is' | 'exclude',
  issue_parent: 'is' as 'is' | 'keyword' | 'none' | 'any',
  issue_status: 'is' as 'is' | 'exclude',
  issue_version: 'is' as 'is' | 'exclude',
  issue_subject: 'contain' as 'contain' | 'start_with' | 'end_with' | 'none' | 'any',

  project_status: 'is' as 'is' | 'exclude',
})

const form = ref<TimeEntryFilter>({
  work_date: '',
  project: '',
  issue: '',
  issue_keyword: '',
  user: null,
  author: null,
  activity: null,
  comment: '',
  tracker: null,
  parent: null,
  status: null,
  version: null,
  subject: '',
  project_status: null,
})

const filterSubmit = () => {
  const filterData = {} as TimeEntryFilter

  // if (cond.value.status === 'open') filterData.status__closed = '0'
  // else if (cond.value.status === 'is') filterData.status = form.value.status
  // else if (cond.value.status === 'exclude') filterData.status__exclude = form.value.status
  // else if (cond.value.status === 'closed') filterData.status__closed = '1'
  // else if (cond.value.status === 'any') filterData.status__closed = ''
  //
  // if (searchCond.value.includes('project'))
  //   if (cond.value.project === 'is') filterData.project__search = form.value.project
  //   else if (cond.value.project === 'exclude') filterData.project__exclude = form.value.project
  //
  // if (searchCond.value.includes('tracker'))
  //   if (cond.value.tracker === 'is') filterData.tracker = form.value.tracker
  //   else if (cond.value.tracker === 'exclude') filterData.tracker__exclude = form.value.tracker

  // if (cond.value.is_public === 'is' && searchCond.value.includes('is_public'))
  //   filterData.is_public = form.value.is_public
  // else if (cond.value.is_public === 'exclude' && searchCond.value.includes('is_public'))
  //   filterData.is_public__exclude = form.value.is_public
  // if (form.value.name) filterData.name = form.value.name
  // if (form.value.description) filterData.description = form.value.description

  emit('filter-submit', filterData)
}

watch(props, nVal => {
  if (nVal.statusList.length) form.value.status = props.statusList[0]?.pk
})

watch(searchCond, nVal => {
  if (nVal.includes('project')) form.value.project = props.allProjects[0]?.slug
  if (nVal.includes('tracker')) form.value.tracker = props.trackerList[0]?.pk
  if (!nVal.includes('work_date')) searchCond.value = ['work_date']
})

const route = useRoute()
onBeforeMount(() => {
  if (!!props.statusList.length) form.value.status = props.statusList[0]?.pk
  if (route.name === '소요시간')
    searchOptions[0].options.splice(0, 0, { value: 'project', label: '프로젝트' })
})
</script>

<template>
  <CRow>
    <CCol class="pointer pt-1 mb-0" @click="condVisible = !condVisible">
      <v-icon :icon="condVisible ? 'mdi-chevron-down' : 'mdi-chevron-right'" size="sm" />
      검색조건
    </CCol>
    <v-divider class="mx-3 mt-2 mb-0" />

    <CCollapse :visible="condVisible">
      <slot name="condition">
        <CRow class="m-2" color="light">
          <CCol class="col-12 col-md-8">
            <CRow>
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck label="작업시간" id="work_date" checked="true" readonly />
              </CCol>
              <CCol class="d-none d-lg-block col-4 col-lg-3 col-xl-2">
                <CFormSelect v-model="cond.work_date" size="sm">
                  <option value="is">이다</option>
                  <option value="<=">이전</option>
                  <option value=">=">이후</option>
                  <option value="between">사이</option>
                  <option value="before_days">일 전</option>
                  <option value="today">오늘</option>
                  <option value="yesterday">어제</option>
                  <option value="this_week">이번 주</option>
                  <option value="last_week">지난 주</option>
                  <option value="this_month">이번 달</option>
                  <option value="last_month">지난 달</option>
                  <option value="this_year">올해</option>
                  <option value="any">모두</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-8 col-lg-3">
                <DatePicker v-model="form.work_date" />
              </CCol>
            </CRow>

            <CRow v-if="searchCond.includes('project')">
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck checked="true" label="프로젝트" id="project" readonly />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect v-model="cond.project" size="sm">
                  <option value="is">이다</option>
                  <option value="exclude">아니다</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3">
                <CFormSelect v-model="form.project" size="sm">
                  <option value="">---------</option>
                  <option v-for="proj in allProjects" :key="proj.pk" :value="proj.slug">
                    <span v-if="proj.parent">{{ '&nbsp;'.repeat(proj.depth) }}</span>
                    {{ proj.name }}
                  </option>
                </CFormSelect>
              </CCol>
            </CRow>

            <CRow v-if="searchCond.includes('issue')">
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck checked="true" label="업무" id="issue" readonly />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect v-model="cond.issue" size="sm">
                  <option value="is">이다</option>
                  <option value="keyword">포함되는 키워드</option>
                  <option value="none">없음</option>
                  <option value="any">모두</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3">
                <Multiselect
                  v-if="cond.issue === 'is'"
                  v-model="form.issue"
                  placeholder="업무 선택"
                />
                <CFormInput
                  v-if="cond.issue === 'keyword'"
                  v-model="form.issue_keyword"
                  tooltip-feedback
                  placeholder="업무 키워드"
                />
              </CCol>
            </CRow>

            <CRow v-if="searchCond.includes('user')">
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck checked="true" label="사용자" id="user" readonly />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect v-model="cond.user" size="sm">
                  <option value="is">이다</option>
                  <option value="exclude">아니다</option>
                  <option value="none">없음</option>
                  <option value="any">모두</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3">
                <Multiselect
                  v-if="cond.user === 'is' || cond.user === 'exclude'"
                  v-model="form.user"
                  placeholder="사용자 선택"
                />
              </CCol>
            </CRow>

            <!--            <CRow v-if="searchCond.includes('created')">-->
            <!--              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">-->
            <!--                <CFormCheck checked="true" label="등록일자" id="created" readonly />-->
            <!--              </CCol>-->
            <!--              <CCol class="col-4 col-lg-3 col-xl-2">-->
            <!--                <CFormSelect size="sm">-->
            <!--                  <option value="1">is</option>-->
            <!--                  <option value="2">&gt;=</option>-->
            <!--                  <option value="3">&lt;=</option>-->
            <!--                  <option value="4">between</option>-->
            <!--                  <option value="5">less than days ago</option>-->
            <!--                  <option value="6">more than days ago</option>-->
            <!--                  <option value="7">is the past</option>-->
            <!--                  <option value="8">days ago</option>-->
            <!--                  <option value="9">today</option>-->
            <!--                  <option value="10">yesterday</option>-->
            <!--                  <option value="11">this week</option>-->
            <!--                  <option value="12">last week</option>-->
            <!--                  <option value="13">last 2 weeks</option>-->
            <!--                  <option value="14">this month</option>-->
            <!--                  <option value="15">last month</option>-->
            <!--                  <option value="16">this year</option>-->
            <!--                  <option value="17">none</option>-->
            <!--                  <option value="18">any</option>-->
            <!--                </CFormSelect>-->
            <!--              </CCol>-->
            <!--              <CCol class="col-4 col-lg-3 col-xl-2">-->
            <!--                <DatePicker size="sm" />-->
            <!--              </CCol>-->
            <!--            </CRow>-->

            <!--            <CRow v-if="searchCond.includes('name')">-->
            <!--              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">-->
            <!--                <CFormCheck checked="true" label="이름" id="name" readonly />-->
            <!--              </CCol>-->
            <!--              <CCol class="col-4 col-lg-3 col-xl-2">-->
            <!--                <CFormSelect v-model="cond.name" size="sm">-->
            <!--                  <option value="contains">contains</option>-->
            <!--                  <option value="2" disabled>contains any of</option>-->
            <!--                  <option value="3" disabled>doesn't contain</option>-->
            <!--                  <option value="4" disabled>starts with</option>-->
            <!--                  <option value="5" disabled>ends with</option>-->
            <!--                  <option value="6" disabled>none</option>-->
            <!--                  <option value="7" disabled>any</option>-->
            <!--                </CFormSelect>-->
            <!--              </CCol>-->
            <!--              <CCol class="col-4 col-lg-3">-->
            <!--                <CFormInput v-model="form.name" size="sm" />-->
            <!--              </CCol>-->
            <!--            </CRow>-->

            <!--            <CRow v-if="searchCond.includes('description')">-->
            <!--              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">-->
            <!--                <CFormCheck checked="true" label="설명" id="description" readonly />-->
            <!--              </CCol>-->
            <!--              <CCol class="col-4 col-lg-3 col-xl-2">-->
            <!--                <CFormSelect v-model="cond.description" size="sm">-->
            <!--                  <option value="contains">contains</option>-->
            <!--                  <option value="2">contains any of</option>-->
            <!--                  <option value="3">doesn't contain</option>-->
            <!--                  <option value="4">starts with</option>-->
            <!--                  <option value="5">ends with</option>-->
            <!--                  <option value="6">none</option>-->
            <!--                  <option value="7">any</option>-->
            <!--                </CFormSelect>-->
            <!--              </CCol>-->
            <!--              <CCol class="col-4 col-lg-3">-->
            <!--                <CFormInput v-model="form.description" size="sm" />-->
            <!--              </CCol>-->
            <!--            </CRow>-->
          </CCol>

          <CCol md="4" class="text-right">
            <CRow>
              <CFormLabel
                for="searchOptions"
                class="col-4 col-lg-2 col-xl-4 col-xxl-5 col-form-label d-block d-md-none d-lg-block"
              >
                검색조건 추가
              </CFormLabel>
              <CCol class="col-8 col-md-12 col-lg-10 col-xl-8 col-xxl-7">
                <Multiselect
                  mode="tags"
                  v-model="searchCond"
                  id="searchOptions"
                  :groups="true"
                  :options="searchOptions"
                  size="sm"
                  class="multiselect-blue"
                  placeholder="검색조건 추가"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </slot>
    </CCollapse>
  </CRow>

  <CRow class="mt-2">
    <CCol class="pointer mb-0" @click="optVisible = !optVisible">
      <v-icon :icon="optVisible ? 'mdi-chevron-down' : 'mdi-chevron-right'" size="sm" />
      옵션
    </CCol>
    <v-divider class="mx-3 mt-2 mb-0" />
    <CCollapse :visible="optVisible">
      <slot name="option">
        <CRow class="m-2" color="light">
          <CCol>
            <span class="mr-3">결과 표시 </span>
            <CFormCheck
              v-model="viewMode"
              label="보드"
              name="viewMode"
              value="board"
              inline
              type="radio"
            />
            <CFormCheck
              v-model="viewMode"
              label="목록"
              name="viewMode"
              value="list"
              inline
              type="radio"
              disabled
            />
          </CCol>
        </CRow>
      </slot>
    </CCollapse>
  </CRow>

  <CRow class="my-3">
    <CCol>
      <slot name="footer">
        <v-icon icon="mdi-check-bold" size="sm" color="success" class="mr-1" />
        <router-link to="" class="mr-3" @click="filterSubmit">검색</router-link>
        <v-icon icon="mdi-replay" size="sm" color="success" class="mr-1" />
        <router-link to="" class="mr-3" @click="resetFilter">초기화</router-link>
        <!--        <router-link to=""> Save 검색양식</router-link>-->
      </slot>
    </CCol>
  </CRow>
</template>
