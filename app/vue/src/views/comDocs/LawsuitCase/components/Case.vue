<script setup lang="ts">
import { computed, PropType } from 'vue'
import { Post } from '@/store/types/document'
import { cutString } from '@/utils/baseMixins'

const props = defineProps({
  suitCase: { type: Object as PropType<Post>, default: null },
})

const sortName = computed(() => props.suitCase.proj_name || '본사')
const sortColor = computed(() => (props.suitCase.project ? 'success' : 'info'))
</script>

<template>
  <CTableRow v-if="suitCase" class="text-center">
    <CTableDataCell>{{ suitCase.pk }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <CBadge :color="sortColor">{{ sortName }}</CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ suitCase.execution_date }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        :to="{ name: '본사 소송사건 - 보기', params: { caseId: suitCase.pk } }"
      >
        {{ cutString(suitCase.title, 30) }}
      </router-link>
      <CBadge v-if="suitCase.is_new" color="warning" size="sm" class="ml-2">
        new
      </CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ suitCase.user }}</CTableDataCell>
    <CTableDataCell>{{ 1 }}</CTableDataCell>
    <CTableDataCell>{{ suitCase.hit }}</CTableDataCell>
  </CTableRow>
</template>
