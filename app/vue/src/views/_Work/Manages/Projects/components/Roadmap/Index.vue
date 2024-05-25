<script lang="ts" setup>
import { onBeforeMount } from 'vue'
import RoadmapList from './components/RoadmapList.vue'

const emit = defineEmits(['aside-visible'])

onBeforeMount(() => emit('aside-visible', true))
</script>

<template>
  <RoadmapList v-if="$route.name === '(로드맵)'" />
</template>
