<script lang="ts" setup>
import { computed } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { ContractRelease } from '@/store/types/contract'
import Pagination from '@/components/Pagination'
import Succession from '@/views/contracts/Succession/components/Succession.vue'
import { TableSecondary } from '@/utils/cssMixins'

const emit = defineEmits(['page-select', 'get-release', 'on-submit'])

const contractStore = useContract()
const contReleaseList = computed(() => contractStore.contReleaseList)
const releasePages = computed(() => contractStore.releasePages)

const pageSelect = (page: number) => emit('page-select', page)
const getRelease = (release: number) => emit('get-release', release)
const onSubmit = (payload: ContractRelease) => emit('on-submit', payload)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="15%" />
      <col width="15%" />
      <col width="11%" />
      <col width="15%" />
      <col width="8%" />
    </colgroup>

    <CTableHead :color="TableSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>계약 정보</CTableHeaderCell>
        <CTableHeaderCell>양도계약자</CTableHeaderCell>
        <CTableHeaderCell>양수계약자</CTableHeaderCell>
        <CTableHeaderCell>승계신청일</CTableHeaderCell>
        <CTableHeaderCell>매매계약일</CTableHeaderCell>
        <CTableHeaderCell>변경인가여부</CTableHeaderCell>
        <CTableHeaderCell>변경인가일</CTableHeaderCell>
        <CTableHeaderCell>확인</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody class="text-center">
      <CTableRow v-for="release in contReleaseList" :key="release.pk">
        <Succession
          :release="release"
          @get-release="getRelease"
          @on-submit="onSubmit"
        />
      </CTableRow>
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="releasePages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
