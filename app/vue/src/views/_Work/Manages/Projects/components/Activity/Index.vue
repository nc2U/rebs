<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useWork } from '@/store/pinia/work'
import NoData from '@/views/_Work/components/NoData.vue'

const emit = defineEmits(['aside-visible'])

const fromDate = computed(
  () =>
    new Date().getFullYear() +
    '/' +
    (new Date().getMonth() + 1) +
    '/' +
    (new Date().getDate() - 10),
)

const toDate = computed(
  () => new Date().getFullYear() + '/' + (new Date().getMonth() + 1) + '/' + new Date().getDate(),
)

const workStore = useWork()
const ActivityLogList = computed(() => workStore.ActivityLogList)

onBeforeMount(() => {
  emit('aside-visible', true)
  workStore.fetchActivityLogList()
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>작업내역</h5>
    </CCol>
  </CRow>

  <CRow class="fst-italic">
    <CCol> {{ fromDate }}부터 {{ toDate }}까지</CCol>
  </CRow>

  <NoData v-if="!ActivityLogList.length" />

  <CRow v-else>
    <CCol v-for="act in ActivityLogList" :key="act.pk">
      {{ act }}
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
