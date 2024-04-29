<script lang="ts" setup>
import { inject, type PropType } from 'vue'
import { type News } from '@/store/types/work'

defineProps({
  newsList: { type: Array as PropType<News[]>, default: () => [] },
})

const isDark = inject('isDark')
</script>

<template>
  <CCard :color="isDark ? '' : 'light'" class="mb-3">
    <CCardBody>
      <CCardSubtitle class="mb-2">
        <v-icon icon="mdi-newspaper" size="sm" color="grey" class="mr-1" />
        최근 뉴스
      </CCardSubtitle>
      <CCardText>
        <div v-for="news in newsList" :key="news.pk">{{ news }} :</div>
      </CCardText>
    </CCardBody>
  </CCard>
</template>
