<script lang="ts" setup>
import { computed, type PropType, ref } from 'vue'
import { useWork } from '@/store/pinia/work_project'
import { useLogging } from '@/store/pinia/work_logging'
import type { IssueProject } from '@/store/types/work_project'
import type { ActLogEntry } from '@/store/types/work_logging'
import Loading from '@/components/Loading/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import ActivityLogList from '@/views/_Work/Manages/Activity/components/ActivityLogList.vue'
import AsideController from '@/views/_Work/Manages/Activity/components/aside/AsideController.vue'

defineProps({
  navMenu: { type: Array as PropType<string[]>, default: () => [] },
  currentProject: { type: Object as PropType<IssueProject | null>, default: null },
  query: { type: Object, default: () => ({}) },
})

const cBody = ref<InstanceType<typeof ContentBody> | null>(null)
const toggle = () => cBody.value?.toggle()
defineExpose({ toggle })

const workStore = useWork()
const hasSubs = computed(() => !!(workStore.currentProject as IssueProject)?.sub_projects?.length)

const toDate = ref(new Date())
const fromDate = computed(() => new Date(toDate.value.getTime() - 9 * 24 * 60 * 60 * 1000))

const logStore = useLogging()
const groupedActivities = computed<{ [key: string]: ActLogEntry[] }>(
  () => logStore.groupedActivities,
)

const toMove = (date: Date) => (toDate.value = date)

const loading = ref<boolean>(true)
</script>

<template>
  <Loading v-model:active="loading" />
  <ContentBody ref="cBody" :nav-menu="navMenu">
    <template v-slot:default>
      <CRow class="py-2">
        <CCol>
          <h5>
            <v-icon
              icon="mdi-history"
              color="green-darken-1"
              size="small"
              class="mr-2"
            />업무실행내역
          </h5>
        </CCol>
      </CRow>

      <ActivityLogList
        :to-date="toDate"
        :from-date="fromDate"
        :activities="groupedActivities"
        @to-move="toMove"
      />
    </template>

    <template v-slot:aside>
      <AsideController
        :to-date="toDate"
        :from-date="fromDate"
        :has-subs="hasSubs"
        @update:to-date="toDate = $event"
        @loading-start="loading = true"
        @loading-end="loading = false"
      />
    </template>
  </ContentBody>
</template>
