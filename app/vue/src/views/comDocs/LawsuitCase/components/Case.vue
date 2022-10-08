<script setup lang="ts">
import { computed, PropType } from 'vue'
import { Post } from '@/store/types/document'
import { cutString } from '@/utils/baseMixins'

const props = defineProps({
  suitCase: { type: Object as PropType<Post>, default: null },
})

const suitCaseName = computed(() => {
  const sCase = props.suitCase
  return `${sCase.court} ${sCase.case_number} ${sCase.case_name}`
})
</script>

<template>
  <CTableRow v-if="suitCase" class="text-center">
    <CTableDataCell>{{ suitCase.sort }}</CTableDataCell>
    <CTableDataCell>{{ suitCase.level }}</CTableDataCell>
    <CTableDataCell>{{ suitCase.related_case }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        :to="{ name: '본사 소송사건 - 보기', params: { caseId: suitCase.pk } }"
      >
        {{ cutString(suitCaseName, 30) }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>{{ suitCase.plaintiff }}</CTableDataCell>
    <CTableDataCell>{{ suitCase.defendant }}</CTableDataCell>
    <CTableDataCell>{{ suitCase.related_debtor }}</CTableDataCell>
  </CTableRow>
</template>
