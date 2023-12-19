<script lang="ts" setup="">
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import UserProfile from '@/views/_MyPage/OwnInfo/components/UserProfile.vue'

const profile = ref({})
const onSubmit = () => 1
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <UserProfile :profile="profile" @on-submit="onSubmit" />
  </ContentBody>
</template>
