<script lang="ts" setup="">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import type { User } from '@/store/types/accounts'
import { type PostFilter, useDocument } from '@/store/pinia/document'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import PostList from '@/views/_MyPage/OwnScrap/components/PostList.vue'

const mainViewName = ref('스크랩')
const userInfo = inject<ComputedRef<User>>('userInfo')

const docStore = useDocument()
const postList = computed(() => docStore.postList)

const fetchPostList = (payload: PostFilter) => docStore.fetchPostList(payload)

onBeforeMount(() => fetchPostList({ user: userInfo?.value.pk }))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <div class="pt-3">
        <PostList :post-list="postList" :view-route="mainViewName" />
      </div>
    </CCardBody>
  </ContentBody>
</template>
