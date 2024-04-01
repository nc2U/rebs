<script lang="ts" setup>
import { ref, type PropType } from 'vue'
import type { Issue, IssueLogEntry, IssueProject } from '@/store/types/work'
import { elapsedTime } from '@/utils/baseMixins'
import { VueMarkdownIt } from '@f3ve/vue-markdown-it'
import IssueControl from './IssueControl.vue'
import IssueHistory from './IssueHistory.vue'
import IssueForm from '@/views/_Work/Manages/Issues/components/IssueForm.vue'

defineProps({
  iProject: { type: Object as PropType<IssueProject>, default: null },
  issue: { type: Object as PropType<Issue>, required: true },
  issueProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
  issueLogList: { type: Array as PropType<IssueLogEntry[]>, default: () => [] },
})

const emit = defineEmits(['on-submit'])

const editForm = ref(false)

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
  }, 100)
}
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>
        <span>{{ issue?.tracker.name }} #{{ issue?.pk }}</span>
        <CBadge color="primary" variant="outline" class="ml-2">진행중</CBadge>
      </h5>
    </CCol>

    <IssueControl @call-edit-form="callEditForm" />
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
            <CCol class="title">시작일 :</CCol>
            <CCol>{{ issue?.start_date }}</CCol>
          </CRow>
          <CRow>
            <CCol class="title">완료일 :</CCol>
            <CCol>{{ issue?.due_date }}</CCol>
          </CRow>
          <CRow>
            <CCol class="title">진척도 :</CCol>
            <CCol>
              <div>
                <CProgress
                  color="success"
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
            <CCol>{{ issue?.estimated_hours ? issue.estimated_hours + ':00 시간' : '' }}</CCol>
          </CRow>
        </CCol>
      </CRow>

      <v-divider />

      <CRow class="mb-3">
        <CCol class="title">설명</CCol>
        <CCol class="text-right form-text">
          <v-icon icon="mdi-comment-text-outline" size="sm" color="grey" class="mr-2" />
          <router-link to="">댓글달기</router-link>
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

  <IssueHistory v-if="issueLogList.length" :issue-log-list="issueLogList" />

  <div>
    <IssueControl @call-edit-form="callEditForm" />
  </div>

  <div v-if="editForm">
    <IssueForm
      :i-project="iProject"
      :issue="issue"
      :issue-projects="issueProjects"
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
