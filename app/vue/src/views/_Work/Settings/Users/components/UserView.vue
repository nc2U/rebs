<script lang="ts" setup>
import { computed, inject, onBeforeMount, type PropType, ref } from 'vue'
import type { ActLogEntry, ActLogEntryFilter, IssueProject } from '@/store/types/work'
import { dateFormat } from '@/utils/baseMixins'
import { useAccount } from '@/store/pinia/account'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import IssueSummary from './atomicViews/IssueSummary.vue'
import ProjectSummary from './atomicViews/ProjectSummary.vue'
import UserActivities from './atomicViews/UserActivities.vue'
import { useWork } from '@/store/pinia/work'

const props = defineProps({
  projectList: { type: Array as PropType<IssueProject[]>, default: () => [] },
  issueNum: {
    type: Object,
    default: () => {},
  },
})

const emit = defineEmits(['aside-visible'])

const superAuth = inject('superAuth', false)

const accStore = useAccount()
const user = computed(() => accStore.user)

const workStore = useWork()
const groupedActivities = computed<{ [key: string]: ActLogEntry[] }>(
  () => workStore.groupedActivities,
)

const issueProjects = computed(() => props.projectList.slice().reverse())

const fetchActivityLogList = (payload: ActLogEntryFilter) => workStore.fetchActivityLogList(payload)

onBeforeRouteUpdate(async to => {
  if (to.params.userId) await accStore.fetchUser(Number(to.params.userId))
  else accStore.user = null
})

const route = useRoute()

onBeforeMount(() => {
  emit('aside-visible', false)
  if (route.params.userId) {
    accStore.fetchUser(Number(route.params.userId))
    fetchActivityLogList({ user: route.params.userId as string })
  }
})
</script>

<template>
  <CRow class="py-2 mb-2">
    <CCol>
      <span class="h5" style="font-size: 1.15em">
        {{ user?.profile?.name ?? user?.username }}
      </span>
    </CCol>

    <CCol v-if="user && superAuth" class="text-right form-text">
      <span class="mr-2">
        <v-icon icon="mdi-pencil" color="amber" size="sm" />
        <router-link :to="{ name: '사용자 - 수정', params: { userId: user.pk } }" class="ml-1">
          편집
        </router-link>
      </span>
    </CCol>
  </CRow>

  <CRow>
    <CCol lg="6">
      <CRow class="mb-3">
        <CCol class="pl-5">
          <ul>
            <li>로그인 : {{ user?.username }}</li>
            <li>등록시각 : {{ user ? dateFormat(user.date_joined, '/') : '' }}</li>
            <li>마지막 로그인 : {{ user?.last_login ? dateFormat(user.last_login, '/') : '' }}</li>
          </ul>
        </CCol>
      </CRow>

      <CRow>
        <CCol>
          <span class="h5" style="font-size: 1.15em">업무</span>
        </CCol>
      </CRow>

      <IssueSummary :issue-num="issueNum" />

      <template v-if="projectList.length">
        <CRow>
          <CCol>
            <span class="h5" style="font-size: 1.15em">프로젝트</span>
          </CCol>
        </CRow>

        <ProjectSummary :project-list="issueProjects" />
      </template>
    </CCol>

    <CCol lg="6" class="pl-2">
      <template v-if="!!groupedActivities">
        <CRow>
          <CCol>
            <h5 style="font-size: 1.15em">
              <router-link :to="{ name: '작업내역' }">작업내역</router-link>
            </h5>
          </CCol>
        </CRow>

        <UserActivities :grouped-activities="groupedActivities" />
      </template>
    </CCol>
  </CRow>
</template>
