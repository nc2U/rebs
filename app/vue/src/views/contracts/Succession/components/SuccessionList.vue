<script lang="ts" setup>
import { computed } from 'vue'
import { usePerms } from '@/composables/usePerms.ts'
import { useContract } from '@/store/pinia/contract'
import { bgLight, TableSecondary } from '@/utils/cssMixins'
import Pagination from '@/components/Pagination'
import Succession from '@/views/contracts/Succession/components/Succession.vue'
import type { Succession as SuccessionType } from '@/store/types/contract'

withDefaults(
  defineProps<{
    highlightId?: number | null
    currentPage?: number
  }>(),
  {
    highlightId: null,
    currentPage: 1,
  },
)

const emit = defineEmits<{
  'page-select': [page: number]
  'call-form': [suc: SuccessionType]
  'done-alert': []
}>()

const { can, PERM } = usePerms()
const canContractSuccession = computed(() => can(PERM.CONTRACT_SUCCESSION))

const contractStore = useContract()
const successionList = computed(() => contractStore.successionList)
const successionPages = computed(() => contractStore.successionPages)

const pageSelect = (page: number) => emit('page-select', page)
const callForm = (suc: SuccessionType) => emit('call-form', suc)
const doneAlert = () => emit('done-alert')
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col style="width: 12%" />
      <col style="width: 12%" />
      <col style="width: 12%" />
      <col style="width: 15%" />
      <col style="width: 15%" />
      <col style="width: 15%" />
      <col style="width: 11%" />
      <col v-if="canContractSuccession" style="width: 8%" />
    </colgroup>

    <CTableHead :color="TableSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>계약 정보</CTableHeaderCell>
        <CTableHeaderCell>양도계약자</CTableHeaderCell>
        <CTableHeaderCell>양수계약자</CTableHeaderCell>
        <CTableHeaderCell>승계신청일</CTableHeaderCell>
        <CTableHeaderCell>매매계약일</CTableHeaderCell>
        <CTableHeaderCell>변경인가일</CTableHeaderCell>
        <CTableHeaderCell>진행상태</CTableHeaderCell>
        <CTableHeaderCell v-if="canContractSuccession">확인</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody>
      <CTableRow v-if="!successionList || successionList.length === 0">
        <CTableDataCell :colspan="canContractSuccession ? 8 : 7" class="text-center py-5 text-muted">
          등록된 권리 의무 승계 내역이 없습니다.
        </CTableDataCell>
      </CTableRow>
      <CTableRow
        v-for="suc in successionList"
        :key="suc.pk"
        :class="suc.status === '3' ? bgLight : ''"
        :color="highlightId === suc.pk ? 'warning' : ''"
        :data-succession-id="suc.pk"
      >
        <Succession
          :succession="suc"
          @call-form="callForm"
          @done-alert="doneAlert"
        />
      </CTableRow>
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="currentPage"
    :limit="8"
    :pages="successionPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
