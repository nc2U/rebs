<script lang="ts" setup>
import { ref, computed, type PropType, onBeforeMount } from 'vue'
import type { Issue, IssueComment, IssueProject, TimeEntry } from '@/store/types/work'
import { elapsedTime, diffDate } from '@/utils/baseMixins'
import { useWork } from '@/store/pinia/work'
import { VueMarkdownIt } from '@f3ve/vue-markdown-it'
import IssueControl from './IssueControl.vue'
import IssueHistory from './IssueHistory.vue'
import IssueForm from '@/views/_Work/Manages/Issues/components/IssueForm.vue'

const props = defineProps({
  iProject: { type: Object as PropType<IssueProject>, default: null },
  issue: { type: Object as PropType<Issue>, required: true },
  allProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
  issueCommentList: { type: Array as PropType<IssueComment[]>, default: () => [] },
  timeEntryList: { type: Array as PropType<TimeEntry[]>, default: () => [] },
})

const emit = defineEmits(['on-submit'])

const issueFormRef = ref()
const editForm = ref(false)

const isClosed = computed(() => props.issue?.closed)

const workStore = useWork()
const issueLogList = computed(() => workStore.issueLogList)

const transTime = (n: number | null) => {
  if (!n) return ''
  else {
    const hours = Math.floor(n)
    const minutes = Math.round((n - hours) * 60)
    const str = minutes >= 10 ? '' : '0'
    return `${hours}:${str}${minutes}`
  }
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

onBeforeMount(async () => await workStore.fetchIssueLogList({ issue: props.issue.pk }))
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
          <!--          <router-link to="">« 뒤로</router-link>-->
          <!--          |-->
          <!--          <router-link to="">2/2</router-link>-->
          <!--          |-->
          <!--          <router-link to="">다음 »</router-link>-->
          <span>« 뒤로 | 2/2 | 다음 »</span>
        </CCol>
      </CRow>

      <CRow>
        <CCol>
          <p class="mt-1 form-text">
            <router-link :to="{ name: '사용자 - 보기', params: { userId: issue.creator.pk } }">
              {{ issue.creator.username }}
            </router-link>
            이(가)
            <router-link
              :to="{
                name: '(작업내역)',
                params: { projId: iProject.slug },
                query: { from: issue?.created.substring(0, 10) },
              }"
            >
              {{ elapsedTime(issue?.created) }}
            </router-link>
            전에 추가함.
            <router-link
              :to="{
                name: '(작업내역)',
                params: { projId: iProject.slug },
                query: { from: issue.updated.substring(0, 10) },
              }"
            >
              {{ elapsedTime(issue.updated) }}
            </router-link>
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
                  :value="issue?.done_ratio ?? 0"
                  style="width: 110px; float: left; margin-top: 2px"
                  height="16"
                />
                <span class="ml-2 pt-0">{{ issue?.done_ratio ?? 0 }}%</span>
              </div>
            </CCol>
          </CRow>
          <CRow>
            <CCol class="title">추정시간:</CCol>
            <CCol v-if="issue?.estimated_hours">{{ transTime(issue?.estimated_hours) }} 시간</CCol>
          </CRow>
          <CRow v-if="issue?.spent_time">
            <CCol class="title">소요시간:</CCol>
            <CCol>
              <router-link :to="{ name: '(소요시간)', query: { issue_id: issue.pk } }">
                {{ transTime(issue?.spent_time) }} 시간
              </router-link>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <v-divider />

      <CRow class="mb-3">
        <CCol class="title">설명</CCol>
        <CCol class="text-right form-text">
          <v-icon icon="mdi-comment-text-outline" size="sm" color="grey" class="mr-2" />
          <router-link to="" @click="callComment">댓글달기</router-link>
        </CCol>
      </CRow>

      <CRow>
        <CCol class="pl-5">
          <VueMarkdownIt :source="issue?.description" />
        </CCol>
      </CRow>

      <v-divider />

      <CRow>
        <CCol class="title">하위 일감</CCol>
        <CCol class="text-right form-text">
          <router-link to="">추가</router-link>
        </CCol>
      </CRow>

      <v-divider />

      <CRow>
        <CCol class="title">연결된 일감</CCol>
        <CCol class="text-right form-text">
          <router-link to="">추가</router-link>
        </CCol>
      </CRow>
    </CCardBody>
  </CCard>

  <IssueHistory
    v-if="issueLogList.length"
    :issue-log-list="issueLogList"
    :issue-comment-list="issueCommentList"
    :time-entry-list="timeEntryList"
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
      :i-project="iProject"
      :issue="issue"
      :all-projects="allProjects"
      @on-submit="onSubmit"
      @close-form="() => (editForm = false)"
    />
  </div>
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
</style>
