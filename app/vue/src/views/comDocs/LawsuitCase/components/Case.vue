<script setup lang="ts">
import { computed, PropType } from 'vue'
import { SuitCase } from '@/store/types/document'
import { cutString } from '@/utils/baseMixins'

const props = defineProps({
  suitCase: { type: Object as PropType<SuitCase>, default: null },
})

const suitCaseName = computed(() => {
  const sCase = props.suitCase
  return `${getCourt(sCase.court_desc as string)} ${sCase.case_number} ${
    sCase.case_name
  }`
})

const relatedCaseName = computed(() =>
  props.suitCase.related_case_name
    ? props.suitCase.related_case_name.split(' ')[1]
    : '',
)

const getCourt = (court: string) =>
  court
    ? court
        .replace('지방법원', '지법')
        .replace('고등법원', '고법')
        .replace('대법원', '대법')
    : ''
</script>

<template>
  <CTableRow v-if="suitCase" class="text-center">
    <CTableDataCell>{{ suitCase.sort_desc }}</CTableDataCell>
    <CTableDataCell>{{ suitCase.level_desc }}</CTableDataCell>
    <CTableDataCell>
      <CCol v-if="suitCase.related_case">
        [
        <router-link
          :to="{
            name: '본사 소송사건',
          }"
        >
          {{ relatedCaseName }}
        </router-link>
        ]
      </CCol>
    </CTableDataCell>
    <CTableDataCell>{{ suitCase.court_desc }}</CTableDataCell>
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
