<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { Rank } from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddRank from './components/AddRank.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import RankList from './components/RankList.vue'

const page = ref<number>(1)
const listControl = ref()

const companyStore = useCompany()
const comName = computed(() => companyStore.company?.name || undefined)

const listFiltering = () => 1

const fetchRankList = (page?: number) => companyStore.fetchRankList(page)

const createRank = (payload: Rank, p: number) =>
  companyStore.createRank(payload, p)
const updateRank = (payload: Rank, p: number) =>
  companyStore.updateRank(payload, p)
const deleteRank = (pk: number) => companyStore.deleteRank(pk)

const multiSubmit = (payload: Rank) => {
  if (!!payload.pk) updateRank(payload, page.value)
  else createRank(payload, page.value)
}
const onDelete = (pk: number) => deleteRank(pk)

const pageSelect = (num: number) => {
  page.value = num
  fetchRankList(num)
}

onMounted(() => fetchRankList())
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
