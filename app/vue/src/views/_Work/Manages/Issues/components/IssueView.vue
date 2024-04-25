<script lang="ts" setup>
import { ref, computed, type PropType, onBeforeMount, watch } from 'vue'
import type {
  CodeValue,
  Issue,
  IssueComment,
  IssueProject,
  IssueRelation,
  IssueStatus,
  TimeEntry,
} from '@/store/types/work'
import { elapsedTime, diffDate, timeFormat, humanizeFileSize, cutString } from '@/utils/baseMixins'
import { useWork } from '@/store/pinia/work'
import { useRoute } from 'vue-router'
import { isValidate } from '@/utils/helper'
import { VueMarkdownIt } from '@f3ve/vue-markdown-it'
import IssueControl from './IssueControl.vue'
import IssueHistory from './IssueHistory.vue'
import IssueForm from '@/views/_Work/Manages/Issues/components/IssueForm.vue'
import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  issueProject: { type: Object as PropType<IssueProject>, default: null },
  issue: { type: Object as PropType<Issue>, required: true },
  allProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
  issueCommentList: { type: Array as PropType<IssueComment[]>, default: () => [] },
  timeEntryList: { type: Array as PropType<TimeEntry[]>, default: () => [] },

  statusList: { type: Array as PropType<IssueStatus[]>, default: () => [] },
  activityList: { type: Array as PropType<CodeValue[]>, default: () => [] },
  priorityList: { type: Array as PropType<CodeValue[]>, default: () => [] },
  getIssues: { type: Array as PropType<{ value: number; label: string }[]>, default: () => [] },
})

const emit = defineEmits(['on-submit'])

const issueFormRef = ref()
const confirmModalRef = ref()
const editForm = ref(false)

const isClosed = computed(() => props.issue?.closed)

const workStore = useWork()
const issueNums = computed(() => workStore.issueNums)
const issueLogList = computed(() => workStore.issueLogList)

const doneRatio = computed(() => {
  if (props.issue?.sub_issues.length) {
    return (
      props.issue.sub_issues.map(sub => sub.done_ratio).reduce((a, b) => a + b) /
      props.issue.sub_issues.length
    )
  } else return props.issue?.done_ratio
})

const estimatedHours = computed(
  () =>
    props.issue.sub_issues.map(s => Number(s.estimated_hours ?? 0)).reduce((a, b) => a + b) +
    (props.issue?.estimated_hours ?? 0),
)

const numToTime = (n: number | null) => {
  const hours = Math.floor(n ?? 0)
  const minutes = Math.round((n ?? 0 - hours) * 60)
  const str = minutes >= 10 ? '' : '0'
  return `${hours}:${str}${minutes}`
}

const onSubmit = (payload: any) => {
  emit('on-submit', payload)
  editForm.value = false
}

const scrollToId = (id: string) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

const callEditForm = () => {
  editForm.value = true

  setTimeout(() => {
    scrollToId('edit-form')
    issueFormRef.value.callComment(true)
  }, 100)
}

const callComment = () => {
  editForm.value = true

  setTimeout(() => {
    scrollToId('edit-form')
    issueFormRef.value.callComment()
  }, 100)
}

const child = ref<number | null>(null)

const parentUnLink = (pk: number) => {
  child.value = pk
  confirmModalRef.value.callModal()
}

const unLinkConfirm = () => {
  workStore.patchIssue(props.issue?.pk, { del_child: child.value })
  child.value = null
  confirmModalRef.value.close()
}

const delSubmit = (pk: number) => workStore.deleteIssueComment(pk, props.issue.pk)

const route = useRoute()
watch(route, async nVal => {
  if (nVal.query.edit) callEditForm()
})

const addRIssue = ref(false)
const validated = ref(false)
const relIssue = ref<IssueRelation>({
  issue: props.issue.pk,
  issue_to: null,
  relation_type: 'relates',
  delay: null,
})
const addRelIssue = (event: Event) => {
  if (isValidate(event)) validated.value = true
  else {
    console.log({ ...relIssue.value })
    workStore.createIssueRelation({ ...relIssue.value })
  }
}
const issueRelationList = computed(() => workStore.issueRelationList)
const relationUnLink = (pk: number) => {}

onBeforeMount(async () => {
  await workStore.fetchIssueLogList({ issue: props.issue.pk })
  if (route.query.edit) callEditForm()
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>
        <span>{{ issue?.tracker.name }} #{{ issue?.pk }}</span>
        <v-badge
          :color="isClosed ? 'success' : 'primary'"
          :content="isClosed ? '완료됨' : '진행중'"
          inline
          rounded="1"
          class="ml-2"
        />
      </h5>
    </CCol>

    <IssueControl
      @call-edit-form="callEditForm"
      @go-time-entry="
        () => $router.push({ name: '(소요시간) - 추가', query: { issue_id: issue.pk } })
      "
    />
  </CRow>

  <CCard color="yellow-lighten-5 mb-3">
    <CCardBody>
      <CRow>
        <CCol>
          <span class="sub-title">{{ issue.subject }}</span>
        </CCol>
        <CCol class="text-right form-text">
          <span v-if="issue.pk === issueNums[0]">« 뒤로</span>
          <router-link
            v-else
            :to="{
              name: '(업무) - 보기',
              params: {
                issueId: issueNums[issueNums.indexOf(issue.pk) - 1],
              },
            }"
            >« 뒤로
          </router-link>
          <span class="mx-2">|</span>
          <router-link :to="{ name: '(업무)' }">
            {{ issueNums.indexOf(issue.pk) + 1 }}/{{ issueNums.length }}
          </router-link>
          <span class="mx-2">|</span>
          <span v-if="issue.pk === issueNums[issueNums.length - 1]">다음 »</span>
          <router-link
            v-else
            :to="{
              name: '(업무) - 보기',
              params: {
                issueId: issueNums[issueNums.indexOf(issue.pk) + 1],
              },
            }"
            >다음 »
          </router-link>
        </CCol>
      </CRow>

      <CRow>
        <CCol>
          <p class="mt-1 form-text">
            <router-link :to="{ name: '사용자 - 보기', params: { userId: issue.creator.pk } }">
              {{ issue.creator.username }}
            </router-link>
            이(가)
            <span>
              <router-link
                :to="{
                  name: '(작업내역)',
                  params: { projId: issueProject?.slug },
                  query: { from: issue?.created.substring(0, 10) },
                }"
              >
                {{ elapsedTime(issue.created) }}
              </router-link>
              <v-tooltip activator="parent" location="top">
                {{ timeFormat(issue.created) }}
              </v-tooltip>
            </span>
            전에 추가함.
            <span>
              <router-link
                :to="{
                  name: '(작업내역)',
                  params: { projId: issueProject.slug },
                  query: { from: issue.updated.substring(0, 10) },
                }"
              >
                {{ elapsedTime(issue.updated) }}
              </router-link>
              <v-tooltip activator="parent" location="top">
                {{ timeFormat(issue?.updated) }}
              </v-tooltip>
            </span>
            전에 수정됨.
          </p>
        </CCol>
      </CRow>

      <CRow>
        <CCol md="6">
          <CRow>
            <CCol class="title">상태 :</CCol>
            <CCol>{{ issue?.status.name }}</CCol>
          </CRow>
          <CRow>
            <CCol class="title">우선순위 :</CCol>
            <CCol>{{ issue?.priority.name }}</CCol>
          </CRow>
          <CRow>
            <CCol class="title">담당자 :</CCol>
            <CCol>
              <router-link
                v-if="issue.assigned_to"
                :to="{ name: '사용자 - 보기', params: { userId: issue?.assigned_to?.pk ?? 0 } }"
              >
                {{ issue?.assigned_to?.username }}
              </router-link>
            </CCol>
          </CRow>
          <CRow>
            <CCol class="title"></CCol>
            <CCol></CCol>
          </CRow>
        </CCol>

        <CCol md="6">
          <CRow>
            <CCol class="title">시작일자 :</CCol>
            <CCol>{{ issue?.start_date }}</CCol>
          </CRow>
          <CRow>
            <CCol class="title">완료기한 :</CCol>
            <CCol
              :class="{
                'text-danger': !isClosed && !!issue.due_date && diffDate(issue.due_date) > 0,
              }"
            >
              {{ issue?.due_date }}
              <span v-if="!isClosed && !!issue.due_date && diffDate(issue.due_date) > 0">
                ({{ Math.floor(diffDate(issue.due_date)) }} 일 지연)
              </span>
            </CCol>
          </CRow>
          <CRow>
            <CCol class="title">진척도 :</CCol>
            <CCol>
              <div>
                <CProgress
                  color="green-lighten-3"
                  :value="doneRatio ?? 0"
                  style="width: 110px; float: left; margin-top: 2px"
                  height="16"
                />
                <span class="ml-2 pt-0">{{ doneRatio ?? 0 }}%</span>
              </div>
            </CCol>
          </CRow>
          <CRow>
            <CCol class="title">추정시간:</CCol>
            <CCol v-if="issue?.sub_issues.length">
              (합계 : {{ numToTime(estimatedHours) }} 시간)
            </CCol>
            <CCol v-else-if="issue?.estimated_hours">
              {{ numToTime(issue?.estimated_hours) }} 시간
            </CCol>
          </CRow>
          <CRow v-if="issue?.spent_time">
            <CCol class="title">소요시간:</CCol>
            <CCol>
              <router-link :to="{ name: '(소요시간)', query: { issue_id: issue.pk } }">
                {{ numToTime(issue?.spent_time) }} 시간
              </router-link>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <v-divider />

      <CRow class="mb-2">
        <CCol class="title">설명</CCol>
        <CCol class="text-right form-text">
          <v-icon icon="mdi-comment-text-outline" size="sm" color="grey" class="mr-2" />
          <router-link to="" @click="callComment">댓글달기</router-link>
        </CCol>
      </CRow>

      <CRow>
        <CCol class="pl-4">
          <VueMarkdownIt :source="issue?.description" />
        </CCol>
      </CRow>

      <v-divider />

      <template v-if="issue.files.length">
        <CRow class="mb-3">
          <CCol>
            <CRow class="mb-2">
              <CCol class="title">파일</CCol>
            </CRow>
            <CRow v-for="(file, i) in issue.files" :key="file.pk">
              <CCol>
                <v-icon icon="mdi-paperclip" size="sm" color="grey" class="mr-2" />
                <span>
                  <a :href="file.file" target="_blank"> {{ file.file_name }} </a>
                </span>
                <span class="file-desc1 mr-1"> ({{ humanizeFileSize(file.file_size) }}) </span>
                <span class="mr-2">
                  <a :href="file.file" target="_blank">
                    <v-icon icon="mdi-download-box" size="16" color="secondary" />
                    <v-tooltip activator="parent" location="top">다운로드</v-tooltip>
                  </a>
                </span>
                <span v-if="file.description" class="mr-2">{{ file.description }}</span>
                <span class="file-desc2 mr-1"> {{ file.user.username }}, </span>
                <span class="file-desc2 mr-2">{{ timeFormat(file.created) }}</span>
                <span>
                  <router-link to="">
                    <v-icon icon="mdi-trash-can-outline" size="16" color="secondary" class="mr-2" />
                    <v-tooltip activator="parent" location="top">삭제</v-tooltip>
                  </router-link>
                </span>
              </CCol>
              <CCol v-if="i === 0" class="text-right form-text">
                <span class="mr-2">
                  <router-link to="">
                    <v-icon icon="mdi-pencil" color="amber" size="18" />
                  </router-link>
                  <v-tooltip activator="parent" location="top">첨부파일 편집</v-tooltip>
                </span>

                <span v-if="issue.files.length > 1" class="mr-2">
                  <router-link to="">
                    <v-icon icon="mdi-download-box" color="secondary" size="18" />
                  </router-link>
                  <v-tooltip activator="parent" location="top">전체 다운로드</v-tooltip>
                </span>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <v-divider />
      </template>

      <CRow class="mb-2">
        <CCol class="col-10">
          <span class="title mr-2">하위 업무</span>
          <template v-if="issue.sub_issues.length">
            <span class="title mr-2">
              <router-link :to="{ name: '(업무)', query: { parent: issue.pk } }">
                {{ issue.sub_issues.length }}
              </router-link>
            </span>
            <span class="form-text">
              (<span v-if="issue.sub_issues.filter(i => !i.closed).length">
                <router-link :to="{ name: '(업무)', query: { parent: issue.pk, status: 'open' } }">
                  {{ issue.sub_issues.filter(i => !i.closed).length }} 건 진행 중
                </router-link>
              </span>
              <span>모두 완료</span>
              -
              <span v-if="issue.sub_issues.filter(i => i.closed).length">
                <router-link
                  :to="{ name: '(업무)', query: { parent: issue.pk, status: 'closed' } }"
                >
                  {{ issue.sub_issues.filter(i => i.closed).length }} 건 완료
                </router-link>
              </span>
              <span v-else>모두 미완료</span>)
            </span>
          </template>
        </CCol>
        <CCol class="text-right form-text">
          <router-link
            :to="{ name: '(업무) - 추가', query: { parent: issue.pk, tracker: issue.tracker.pk } }"
          >
            추가
          </router-link>
        </CCol>
      </CRow>

      <template v-if="issue.sub_issues.length">
        <CRow v-for="sub in issue.sub_issues" :key="sub.pk">
          <CCol md="6" lg="4">
            <router-link
              :to="{ name: '(업무) - 보기', params: { issueId: sub.pk } }"
              :class="{ closed: sub.closed }"
            >
              기능 #{{ sub.pk }}
            </router-link>
            : {{ sub.subject }}
          </CCol>
          <CCol class="col-sm-6 col-md-3 col-lg-4 text-right">
            <span class="mr-3">{{ sub.status }}</span>
            <span v-if="sub.assigned_to" class="mr-3">
              <router-link :to="{ name: '사용자 - 보기', params: { userId: sub.assigned_to.pk } }">
                {{ cutString(sub.assigned_to.username, 9) }}
              </router-link>
            </span>
            <span class="mr-3">{{ sub?.start_date }}</span>
          </CCol>
          <CCol class="col-sm-6 col-md-3 col-lg-4 text-right">
            <span class="mr-3">
              <CProgress
                color="green-lighten-3"
                :value="sub?.done_ratio ?? 0"
                style="width: 100px; float: left; margin-top: 3px"
                height="14"
              />
            </span>
            <span class="mr-3" @click="parentUnLink(sub.pk)">
              <v-icon icon="mdi-link-variant-off" size="sm" color="grey" class="pointer" />
              <v-tooltip activator="parent" location="top"> 관계 지우기 </v-tooltip>
            </span>
            <span>
              <CDropdown color="secondary" variant="input-group" placement="bottom-end">
                <CDropdownToggle
                  :caret="false"
                  color="light"
                  variant="ghost"
                  size="sm"
                  shape="rounded-pill"
                >
                  <v-icon icon="mdi-dots-horizontal" class="pointer" color="grey-darken-1" />
                  <v-tooltip activator="parent" location="top">Actions</v-tooltip>
                </CDropdownToggle>
                <CDropdownMenu>
                  <CDropdownItem
                    class="form-text"
                    @click="
                      $router.push({
                        name: '(업무) - 보기',
                        params: { issueId: sub.pk },
                        query: { edit: '1' },
                      })
                    "
                  >
                    <router-link to="">
                      <v-icon icon="mdi-pencil" color="amber" size="sm" />
                      편집
                    </router-link>
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon color="amber" size="sm" />
                    유형
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <v-icon color="amber" size="sm" />
                    <!--                    <router-link to=""> -->
                    우선순위
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <v-icon color="amber" size="sm" />
                    <!--                    <router-link to=""> -->
                    담당자
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <v-icon color="amber" size="sm" />
                    <!--                    <router-link to=""> -->
                    진척도
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-star" color="secondary" size="sm" />
                    지켜보기
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-timer-edit-outline" color="grey" size="sm" />
                    작업시간 기록
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-link-plus" color="grey" size="sm" />
                    링크 복사
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-content-copy" color="grey" size="sm" />
                    복사
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-trash-can-outline" color="grey" size="sm" />
                    업무 삭제
                    <!--                    </router-link>-->
                  </CDropdownItem>
                </CDropdownMenu>
              </CDropdown>
            </span>
          </CCol>
        </CRow>
      </template>

      <v-divider />

      <CRow>
        <CCol class="col-10 title">
          <span class="title mr-2">연결된 업무</span>
        </CCol>
        <CCol class="text-right form-text">
          <router-link to="" @click="addRIssue = !addRIssue">추가</router-link>
        </CCol>
      </CRow>

      <div v-if="issueRelationList.length" class="mt-2">
        <CRow v-for="rel in issueRelationList" :key="rel.pk">
          <CCol md="6">
            <span>{{ rel.type_display }} : </span>
            <span>
              <router-link :to="{ name: '(업무) - 보기', params: { issueId: rel.issue_to?.pk } }">
                기능 #{{ rel.issue_to?.pk }}
              </router-link>
              : {{ rel.issue_to?.subject }}
            </span>
          </CCol>
          <CCol class="col-sm-8 col-md-3 text-right">
            <span class="mr-3">{{ rel.issue_to?.status }}</span>
            <span v-if="rel.issue_to" class="mr-3">
              <router-link
                :to="{ name: '사용자 - 보기', params: { userId: rel.issue_to.assigned_to.pk } }"
              >
                {{ cutString(rel.issue_to.assigned_to.username, 9) }}
              </router-link>
            </span>
            <span class="mr-3">{{ rel.issue_to?.start_date }}</span>
          </CCol>
          <CCol class="col-sm-4 col-md-3 text-right">
            <span class="mr-3">
              <CProgress
                color="green-lighten-3"
                :value="rel.issue_to?.done_ratio"
                style="width: 100px; float: left; margin-top: 3px"
                height="14"
              />
            </span>
            <span class="mr-3" @click="relationUnLink(rel.issue_to?.pk as number)">
              <v-icon icon="mdi-link-variant-off" size="sm" color="grey" class="pointer" />
              <v-tooltip activator="parent" location="top"> 관계 지우기 </v-tooltip>
            </span>
            <span>
              <CDropdown color="secondary" variant="input-group" placement="bottom-end">
                <CDropdownToggle
                  :caret="false"
                  color="light"
                  variant="ghost"
                  size="sm"
                  shape="rounded-pill"
                >
                  <v-icon icon="mdi-dots-horizontal" class="pointer" color="grey-darken-1" />
                  <v-tooltip activator="parent" location="top">Actions</v-tooltip>
                </CDropdownToggle>
                <CDropdownMenu>
                  <CDropdownItem
                    class="form-text"
                    @click="
                      $router.push({
                        name: '(업무) - 보기',
                        params: { issueId: rel.issue_to?.pk },
                        query: { edit: '1' },
                      })
                    "
                  >
                    <router-link to="">
                      <v-icon icon="mdi-pencil" color="amber" size="sm" />
                      편집
                    </router-link>
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon color="amber" size="sm" />
                    유형
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <v-icon color="amber" size="sm" />
                    <!--                    <router-link to=""> -->
                    우선순위
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <v-icon color="amber" size="sm" />
                    <!--                    <router-link to=""> -->
                    담당자
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <v-icon color="amber" size="sm" />
                    <!--                    <router-link to=""> -->
                    진척도
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-star" color="secondary" size="sm" />
                    지켜보기
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-timer-edit-outline" color="grey" size="sm" />
                    작업시간 기록
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-link-plus" color="grey" size="sm" />
                    링크 복사
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-content-copy" color="grey" size="sm" />
                    복사
                    <!--                    </router-link>-->
                  </CDropdownItem>
                  <CDropdownItem class="form-text" disabled>
                    <!--                    <router-link to="">-->
                    <v-icon icon="mdi-trash-can-outline" color="grey" size="sm" />
                    업무 삭제
                    <!--                    </router-link>-->
                  </CDropdownItem>
                </CDropdownMenu>
              </CDropdown>
            </span>
          </CCol>
        </CRow>
      </div>

      <CForm
        class="needs-validation"
        novalidate
        :validated="validated"
        @submit.prevent="addRelIssue"
      >
        <CRow v-if="addRIssue">
          <CCol sm="4" md="3" lg="2">
            <CFormSelect v-model="relIssue.relation_type">
              <option value="relates">다음 업무와 관련됨 :</option>
              <option value="duplicates">다음 업무에 중복됨 :</option>
              <option value="duplicated">중복된 업무 :</option>
              <option value="blocks">다음 업무의 해결을 막고 있음 :</option>
              <option value="blocked">다음 업무에게 막혀 있음 :</option>
              <option value="precedes">다음에 진행할 업무 :</option>
              <option value="follows">다음 업무를 우선 진행 :</option>
              <option value="copied_to">다음 업무로 복사됨 :</option>
              <option value="copied_from">다음 업무로부터 복사됨 :</option>
            </CFormSelect>
          </CCol>
          <CFormLabel for="colFormLabel" class="col-sm-1 col-form-label text-right">
            업무 #
          </CFormLabel>
          <CCol sm="4" md="3" lg="2">
            <Multiselect
              v-model="relIssue.issue_to"
              :options="getIssues"
              :classes="{
                caret: 'multiselect-caret mr-4',
                search: 'form-control multiselect-search',
                tagsSearch: 'form-control multiselect-tags-search',
              }"
              :attrs="relIssue.issue_to ? {} : { required: true }"
              placeholder="업무 검색"
              :add-option-on="['enter', 'tab']"
              searchable
            />
          </CCol>
          <template
            v-if="relIssue.relation_type === 'precedes' || relIssue.relation_type === 'follows'"
          >
            <CFormLabel for="colFormLabel" class="col-sm-1 col-form-label text-right">
              지연 :
            </CFormLabel>
            <CCol sm="3" md="2" lg="1">
              <CFormInput v-model="relIssue.delay" />
            </CCol>
            <CFormLabel class="col-sm-1 col-form-label"> 일</CFormLabel>
          </template>
          <CCol class="pt-1">
            <CButton type="submit" color="primary" size="sm">추가</CButton>
            <CButton color="light" size="sm" @click="addRIssue = false">취소</CButton>
          </CCol>
        </CRow>
      </CForm>
    </CCardBody>
  </CCard>

  <IssueHistory
    v-if="issueLogList.length"
    :issue-log-list="issueLogList"
    :issue-comment-list="issueCommentList"
    :time-entry-list="timeEntryList"
    @del-submit="delSubmit"
  />

  <div>
    <IssueControl
      @call-edit-form="callEditForm"
      @go-time-entry="() => $router.push({ name: '(소요시간) - 추가', query: { issue_id: 1 } })"
    />
  </div>

  <div v-if="editForm">
    <IssueForm
      ref="issueFormRef"
      :issue-project="issueProject"
      :issue="issue"
      :all-projects="allProjects"
      :status-list="statusList"
      :activity-list="activityList"
      :priority-list="priorityList"
      :get-issues="getIssues"
      @on-submit="onSubmit"
      @close-form="() => (editForm = false)"
    />
  </div>

  <ConfirmModal ref="confirmModalRef">
    <template #header>관계 지우기 확인</template>
    <template #default> 계속 진행하시겠습니까?</template>
    <template #footer>
      <CButton color="warning" @click="unLinkConfirm">확인</CButton>
    </template>
  </ConfirmModal>
</template>

<style lang="scss" scoped>
.title {
  font-weight: bold;
}

.sub-title {
  font-size: 1.1em;
  font-weight: bold;
  color: #0f192a;
}

.file-desc1 {
  font-size: 0.9em;
  color: #777;
}

.file-desc2 {
  font-size: 0.85em;
  color: #888;
}

.closed {
  color: #999;
  text-decoration: line-through;
}
</style>
