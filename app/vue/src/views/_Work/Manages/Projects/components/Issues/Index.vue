<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useWork } from '@/store/pinia/work'

const emit = defineEmits(['aside-visible'])

const workStore = useWork()
const issueList = computed(() => workStore.issueList)

onBeforeMount(() => {
  emit('aside-visible', true)
  workStore.fetchIssueList()
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>{{ $route.name }}</h5>
    </CCol>
  </CRow>
</template>
