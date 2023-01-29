<script lang="ts" setup>
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddRank from './components/AddRank.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import RankList from './components/RankList.vue'

const msg = ref(pageTitle)
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody>
    <CCardBody>
      <ListController />
      <AddRank />
      <TableTitleRow title="직급 목록" excel url="#" disabled />
      <RankList />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
