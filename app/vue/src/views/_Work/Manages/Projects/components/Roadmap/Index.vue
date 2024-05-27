<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import RoadmapList from './components/RoadmapList.vue'
import VersionView from './components/VersionView.vue'
import VersionForm from './components/VersionForm.vue'

const emit = defineEmits(['aside-visible'])

const workStore = useWork()
const versionList = computed(() => workStore.versionList)

const [route, router] = [useRoute(), useRouter()]
const onSubmit = (payload: any, back = false) => {
  if (!payload.pk) {
    payload.project = route.params.projId as string
    workStore.createVersion(payload)
    if (!back) router.replace({ name: '(로드맵)' })
  } else workStore.updateVersion(payload)
  if (back) router.replace({ name: '(설정)', query: { menu: '버전' } })
}

onBeforeMount(() => {
  emit('aside-visible', true)
  workStore.fetchVersionList()
})
</script>

<template>
  <RoadmapList v-if="route.name === '(로드맵)'" :version-list="versionList" />

  <VersionView v-if="route.name === '(로드맵) - 보기'" />

  <VersionForm
    v-if="route.name === '(로드맵) - 추가' || route.name === '(로드맵) - 수정'"
    @on-submit="onSubmit"
  />
</template>
