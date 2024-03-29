<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { dateFormat, timeFormat } from '@/utils/baseMixins'
import { useWork } from '@/store/pinia/work'
import type { ActLogEntry } from '@/store/types/work'
import NoData from '@/views/_Work/components/NoData.vue'

const emit = defineEmits(['aside-visible'])

const toDate = ref(new Date())
watch(toDate, nVal => {
  workStore.fetchActivityLogList({
    from_act_date: dateFormat(fromDate.value),
    to_act_date: dateFormat(nVal),
  })
})

const fromDate = computed(() => new Date(toDate.value.getTime() - 10 * 24 * 60 * 60 * 1000))

const workStore = useWork()
const groupedActivities = computed<{ [key: string]: ActLogEntry[] }>(
  () => workStore.groupedActivities,
)

onBeforeMount(() => {
  emit('aside-visible', true)
  workStore.fetchActivityLogList({
    from_act_date: dateFormat(fromDate.value),
    to_act_date: dateFormat(toDate.value),
  })
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>작업내역</h5>
    </CCol>
  </CRow>

  <CRow class="fst-italic">
    <CCol> {{ dateFormat(fromDate, '/') }}부터 {{ dateFormat(toDate, '/') }}까지</CCol>
  </CRow>

  <NoData v-if="!groupedActivities" />

  <CRow v-else class="my-3">
    <CCol v-for="(val, key) in groupedActivities" :key="key">
      <CAlert color="secondary" class="px-3 py-2">
        <span class="date-title">{{ String(key) === dateFormat(new Date()) ? '오늘' : key }}</span>
      </CAlert>

      <div v-for="act in val" :key="act.pk">
        <span>{{ timeFormat(act.timestamp, true) }}</span>
        <span class="ml-2">{{ act.project }}</span> -
        <span>{{ act.issue }}</span>
        <div>{{ act.user.username }}</div>
        <v-divider class="my-2" />
        {{ act }}
      </div>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CButtonGroup role="group">
        <CButton color="primary" variant="outline" size="sm">« 뒤로</CButton>
        <CButton color="primary" variant="outline" size="sm">다음 »</CButton>
      </CButtonGroup>
    </CCol>
  </CRow>
</template>

<style lang="scss" scoped>
.date-title {
  font-size: 1.2em;
  font-weight: bold;
}
</style>
