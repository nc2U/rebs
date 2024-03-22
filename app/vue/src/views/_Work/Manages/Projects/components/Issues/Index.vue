<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import IssueList from './components/IssueList.vue'
import IssueView from './components/IssueView.vue'

const emit = defineEmits(['aside-visible'])

const route = useRoute()

const workStore = useWork()
const issueList = computed(() => workStore.issueList)
onBeforeMount(() => {
  emit('aside-visible', true)
  workStore.fetchIssueList()
})
</script>

<template>
  <IssueList v-if="route.name === '(업무)'" :issue-list="issueList" />

  <IssueView v-if="route.name === '(업무) - 보기'" />
</template>
