<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddRank from './components/AddRank.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import RankList from './components/RankList.vue'

const listControl = ref()

const companyStore = useCompany()
const fetchRankList = (page?: number) => companyStore.fetchRankList(page)

const listFiltering = () => 1
const pageSelect = (page: number) => fetchRankList(page)

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
      <AddRank />
      <TableTitleRow title="직급 목록" excel url="#" disabled />
      <RankList @page-select="pageSelect" />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
