<script lang="ts" setup>
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddDepartment from './components/AddDepartment.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import DepartmentList from './components/DepartmentList.vue'

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
      <AddDepartment />
      <TableTitleRow title="부서 목록" excel url="#" disabled />
      <DepartmentList />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
