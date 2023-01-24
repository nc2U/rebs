<script lang="ts" setup>
// import { computed } from 'vue'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { useStore } from 'vuex'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UserSelect from './components/UserSelect.vue'
import ProjectManageAuth from './components/ProjectManageAuth.vue'
import SideBarManageAuth from './components/SideBarManageAuth.vue'

const store = useStore()
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody>
    <CCardBody>
      <UserSelect />
      <ProjectManageAuth />
      <SideBarManageAuth />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
