<script lang="ts" setup>
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddStaff from './components/AddStaff.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import StaffList from './components/StaffList.vue'

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
      <AddStaff />
      <TableTitleRow title="직원 목록" excel url="#" disabled />
      <StaffList />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
