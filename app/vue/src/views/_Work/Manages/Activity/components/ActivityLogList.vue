<script lang="ts" setup>
import type { PropType } from 'vue'
import { dateFormat, timeFormat } from '@/utils/baseMixins'
import { VueMarkdownIt } from '@f3ve/vue-markdown-it'
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

const emit = defineEmits(['to-back', 'to-next'])
const toBack = () => emit('to-back')
const toNext = () => emit('to-next')
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
    <CCol>
      <CRow v-for="(val, key) in groupedActivities" :key="key">
        <CAlert color="secondary" class="px-3 py-2">
          <span class="date-title">{{
            String(key) === dateFormat(new Date()) ? '오늘' : key
          }}</span>
        </CAlert>

        <div v-for="act in val" :key="act.pk" class="pl-5">
          <div>
            <v-icon icon="mdi-cog" size="sm" color="warning" class="mr-1" />
            <span class="form-text">{{ timeFormat(act.timestamp, true) }}</span>
            <span class="ml-2 bold">{{ act.project }}</span> -
            <span v-if="act.issue">
              <router-link to="">
                {{ act.issue.tracker }} #{{ act.pk }} ({{ act.status_log || act.issue.status }})
                {{ act.issue.subject }}
              </router-link>
            </span>
          </div>
          <div class="ml-4 pl-5">
            <VueMarkdownIt :source="act.issue?.description" class="form-text" />
          </div>
          <div class="form-text ml-5 pl-2 bg-amber-accent-2">
            <router-link to="">{{ act.user.username }}</router-link>
          </div>
          <v-divider class="my-2" />
        </div>
      </CRow>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CButtonGroup role="group">
        <CButton color="primary" variant="outline" size="sm" @click="toBack">« 뒤로</CButton>
        <CButton color="primary" variant="outline" size="sm" @click="toNext">다음 »</CButton>
      </CButtonGroup>
    </CCol>
  </CRow>
</template>

<style lang="scss" scoped>
.date-title {
  font-size: 1.2em;
  font-weight: bold;
}

ol {
  margin-bottom: 0 !important;
  padding-bottom: 0 !important;
}
</style>
