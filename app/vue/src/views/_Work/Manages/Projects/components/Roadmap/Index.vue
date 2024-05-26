<script lang="ts" setup>
import { onBeforeMount } from 'vue'
import RoadmapList from './components/RoadmapList.vue'
import VersionForm from './components/VersionForm.vue'

const emit = defineEmits(['aside-visible'])

onBeforeMount(() => emit('aside-visible', true))
</script>

<template>
  <RoadmapList v-if="$route.name === '(로드맵)'" />

  <VersionForm v-if="$route.name === '(로드맵) - 추가'" />
</template>
