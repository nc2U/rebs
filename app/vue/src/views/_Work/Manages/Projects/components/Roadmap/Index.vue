<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useWork } from '@/store/pinia/work'
import RoadmapList from './components/RoadmapList.vue'
import VersionView from './components/VersionView.vue'
import VersionForm from './components/VersionForm.vue'

const emit = defineEmits(['aside-visible'])

const workStore = useWork()
const versionList = computed(() => workStore.versionList)

onBeforeMount(() => {
  emit('aside-visible', true)
  workStore.fetchVersionList()
})
</script>

<template>
  <RoadmapList v-if="$route.name === '(로드맵)'" :version-list="versionList" />

  <VersionView v-if="$route.name === '(로드맵) - 보기'" />

  <VersionForm v-if="$route.name === '(로드맵) - 추가'" />
</template>
