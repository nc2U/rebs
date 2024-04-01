<script lang="ts" setup>
import type { PropType } from 'vue'
import { dateFormat, timeFormat, cutString } from '@/utils/baseMixins'
import { VueMarkdownIt } from '@f3ve/vue-markdown-it'
import type { ActLogEntry } from '@/store/types/work'
import NoData from '@/views/_Work/components/NoData.vue'

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

  <NoData v-if="!Object.getOwnPropertyNames(groupedActivities).length" />

  <CRow v-else class="my-3">
    <CCol>
      <CRow v-for="(val, key) in groupedActivities" :key="key">
        <CCol>
          <CAlert color="secondary" class="px-3 py-2">
            <span class="date-title">
              {{ String(key) === dateFormat(new Date()) ? '오늘' : dateFormat(key as string, '/') }}
            </span>
          </CAlert>

          <CRow v-for="(act, i) in val" :key="act.pk" class="pl-3">
            <CCol :class="{ 'ml-5': i }">
              <v-icon icon="mdi-folder-plus" size="sm" color="warning" class="mr-1" />
              <span class="form-text mr-2">{{ timeFormat(act.timestamp, true) }}</span>
              <span v-if="!$route.params.projId">{{ act.project?.name }} - </span>
              <span v-if="act.issue">
                <router-link
                  :to="{
                    name: '(업무) - 보기',
                    params: { projId: act.project?.slug, issueId: act.issue.pk },
                  }"
                >
                  {{ act.issue.tracker }} #{{ act.issue.pk }} ({{
                    act.status_log || act.issue.status
                  }})
                  {{ act.issue.subject }}
                </router-link>
              </span>

              <div class="ml-4 pl-5 fst-italic">
                <VueMarkdownIt
                  v-if="act.sort === '1' && act.action === 'Created'"
                  :source="cutString(act.issue?.description, 113)"
                  class="form-text"
                />
              </div>
              <div v-if="act.user" class="form-text ml-5 pl-2">
                <router-link to="">{{ act.user.username }}</router-link>
              </div>
              <v-divider class="my-2" />
            </CCol>
          </CRow>
        </CCol>
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
</style>
