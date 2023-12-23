<script lang="ts" setup="">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import { useRoute } from 'vue-router'
import type { User } from '@/store/types/accounts'
import { type PostFilter, useDocument } from '@/store/pinia/document'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import PostList from '@/views/_MyPage/OwnPost/components/PostList.vue'

const mainViewName = ref('내 작성글')
const userInfo = inject<ComputedRef<User>>('userInfo')

const postFilter = ref<PostFilter>({
  user: '',
  search: '',
  page: 1,
})

const listFiltering = (payload: PostFilter) => {
  postFilter.value.user = payload.user
  postFilter.value.search = payload.search
}

const docStore = useDocument()
const postList = computed(() => docStore.postList)

const fetchPost = (pk: number) => docStore.fetchPost(pk)
const fetchPostList = (payload: PostFilter) => docStore.fetchPostList(payload)

const route = useRoute()

const dataSetup = (pk: number, postId?: string | string[]) => {
  postFilter.value.user = pk
  fetchPostList(postFilter.value)
  if (postId) fetchPost(Number(postId))
}

onBeforeMount(() => dataSetup(userInfo?.value.pk as number, route.params?.postId))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <PostList :post-list="postList" :view-route="mainViewName" />
    </CCardBody>
  </ContentBody>
</template>
