<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { Rank, RankFilter } from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddRank from './components/AddRank.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import RankList from './components/RankList.vue'

const listControl = ref()

const dataFilter = ref<RankFilter>({
  page: 1,
  com: 1,
  sort: '',
  q: '',
})

const companyStore = useCompany()
const initComId = computed(() => companyStore.initComId)
const comId = computed(() => companyStore.company?.pk || initComId.value)
const comName = computed(() => companyStore.company?.name || undefined)

onMounted(() => fetchRankList({}))

const listFiltering = (payload: RankFilter) => {
  dataFilter.value = payload
  fetchRankList({
    page: payload.page,
    com: payload.com,
    sort: payload.sort,
    q: payload.q,
  })
}

const fetchRankList = (payload: RankFilter) =>
  companyStore.fetchRankList(payload)

const createRank = (payload: Rank, p?: number, c?: number) =>
  companyStore.createRank(payload, p, c)
const updateRank = (payload: Rank, p?: number, c?: number) =>
  companyStore.updateRank(payload, p, c)
const deleteRank = (pk: number, com: number) => companyStore.deleteRank(pk, com)

const multiSubmit = (payload: Rank) => {
  const { page } = dataFilter.value
  if (!!payload.pk) updateRank(payload, page, comId.value)
  else createRank(payload, page, comId.value)
}
const onDelete = (pk: number) => deleteRank(pk, comId.value)

const pageSelect = (num: number) => {
  dataFilter.value.page = num
  dataFilter.value.com = comId.value
  fetchRankList(dataFilter.value)
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody>
    <CCardBody>
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddRank :company="comName" @multi-submit="multiSubmit" />
      <TableTitleRow title="직급 목록" excel url="#" disabled />
      <RankList
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @page-select="pageSelect"
      />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
