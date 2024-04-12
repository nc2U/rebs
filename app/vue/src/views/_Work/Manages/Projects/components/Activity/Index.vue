<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { dateFormat } from '@/utils/baseMixins'
import { useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import type { ActLogEntry } from '@/store/types/work'
import ActivityLogList from '@/views/_Work/Manages/Activity/components/ActivityLogList.vue'

const emit = defineEmits(['aside-visible'])

const workStore = useWork()
const groupedActivities = computed<{ [key: string]: ActLogEntry[] }>(
  () => workStore.groupedActivities,
)

const fromDate = computed(() => new Date(toDate.value.getTime() - 10 * 24 * 60 * 60 * 1000))

const toDate = ref(new Date())
watch(toDate, nVal => {
  workStore.fetchActivityLogList({
    from_act_date: dateFormat(fromDate.value),
    to_act_date: dateFormat(nVal),
  })
})

const toBack = () => (toDate.value = new Date(toDate.value.setDate(toDate.value.getDate() - 10)))
const toNext = () => (toDate.value = new Date(toDate.value.setDate(toDate.value.getDate() + 10)))

const route = useRoute()

onBeforeMount(() => {
  emit('aside-visible', true)
  if (route.params.projId) {
    workStore.fetchIssueProject(route.params.projId as string)
    workStore.fetchActivityLogList({
      project: route.params.projId,
      from_act_date: dateFormat(fromDate.value),
      to_act_date: dateFormat(toDate.value),
    })
  }
})
</script>

<template>
  <ActivityLogList
    :grouped-activities="groupedActivities"
    :from-date="fromDate"
    :to-date="toDate"
    @to-back="toBack"
    @to-next="toNext"
  />
</template>
