<script lang="ts" setup>
import { navMenu, pageTitle } from '@/views/_MyPage/_menu/headermixin'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import UserProfile from '@/views/_MyPage/OwnInfo/components/UserProfile.vue'
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <UserProfile />
  </ContentBody>
</template>
