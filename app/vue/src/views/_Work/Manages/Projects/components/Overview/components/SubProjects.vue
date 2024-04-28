<script lang="ts" setup="">
import { inject, type PropType } from 'vue'
import type { IssueProject } from '@/store/types/work'

defineProps({
  subProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
})

const isDark = inject('isDark')
</script>

<template>
  <CCard :color="isDark ? '' : 'light'" class="mb-3">
    <CCardBody>
      <CCardSubtitle>하위 프로젝트</CCardSubtitle>
      <CCardText>
        <router-link
          v-for="(sub, i) in subProjects"
          :to="{ name: '(개요)', params: { projId: sub.slug } }"
          :key="sub.pk"
        >
          {{ sub.name }}<span v-if="i + 1 < subProjects?.length">, </span>
        </router-link>
      </CCardText>
    </CCardBody>
  </CCard>
</template>
