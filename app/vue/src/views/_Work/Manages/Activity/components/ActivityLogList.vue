<script lang="ts" setup>
import type { PropType } from 'vue'
import { dateFormat, timeFormat } from '@/utils/baseMixins'
import type { ActLogEntry } from '@/store/types/work'

defineProps({
  groupedActivities: {
    type: Object as PropType<{ [key: string]: ActLogEntry[] }>,
    default: () => {},
  },
  fromDate: {
    type: Object as PropType<Date>,
    default: () => {},
  },
  toDate: {
    type: Object as PropType<Date>,
    default: () => {},
  },
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
