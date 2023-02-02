<script setup lang="ts">
import { computed, PropType } from 'vue'
import { useStore } from 'vuex'
import { SuitCase } from '@/store/types/document'
import { cutString } from '@/utils/baseMixins'

const props = defineProps({
  suitCase: { type: Object as PropType<SuitCase>, default: null },
})

const emit = defineEmits([
  'agency-filter',
  'agency-search',
  'related-filter',
  'sort-filter',
])

const suitCaseName = computed(() => {
  const sCase = props.suitCase
  return `${getCourt(sCase.court_desc as string)} ${sCase.case_number} ${
    sCase.case_name
  }`
})

const store = useStore()
const sortName = computed(() => props.suitCase.proj_name || '본사')
const sortColor = computed(() => (props.suitCase.project ? 'success' : 'info'))
const courtColor = computed(() =>
  store.state.theme !== 'dark' ? 'dark' : 'default',
)
const agencyName = computed(() => {
  const agency = props.suitCase.court_desc || props.suitCase.other_agency
  return agency ? getCourt(agency) : ''
})
const relatedCaseName = computed(() =>
  props.suitCase.related_case_name
    ? props.suitCase.related_case_name.split(' ')[1]
    : '',
)

const agencyFunc = computed(() =>
  props.suitCase.court_desc !== ''
    ? emit('agency-filter', props.suitCase.court)
    : emit('agency-search', props.suitCase.other_agency),
)

const sortFunc = () => emit('sort-filter', props.suitCase.project)
const relatedFilter = () => emit('related-filter', props.suitCase.related_case)
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
    <CTableDataCell class="text-left">
      <a href="javascript:void(0);" @click="sortFunc">
        <CBadge :color="sortColor" shape="rounded-pill">{{ sortName }}</CBadge>
      </a>
    </CTableDataCell>
    <CTableDataCell>{{ suitCase.sort_desc }}</CTableDataCell>
    <CTableDataCell>{{ suitCase.level_desc }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <span v-if="suitCase.court_desc || suitCase.other_agency">
        <a href="javascript:void(0);" @click="agencyFunc">
          <CBadge :color="courtColor" shape="rounded-pill">
            {{ agencyName }}
          </CBadge>
        </a>
      </span>
    </CTableDataCell>
    <CTableDataCell>
      <CCol v-if="suitCase.related_case">
        [
        <a href="javascript:void(0);" @click="relatedFilter">
          {{ relatedCaseName }}
        </a>
        ]
      </CCol>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        :to="{ name: '본사 소송 사건 - 보기', params: { caseId: suitCase.pk } }"
      >
        {{ cutString(suitCaseName, 28) }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>{{ suitCase.plaintiff }}</CTableDataCell>
    <CTableDataCell>{{ suitCase.defendant }}</CTableDataCell>
    <CTableDataCell>{{ suitCase.related_debtor }}</CTableDataCell>
  </CTableRow>
</template>
