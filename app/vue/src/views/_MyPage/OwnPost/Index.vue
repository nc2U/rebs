<script lang="ts" setup="">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import type { User } from '@/store/types/accounts'
import { type PostFilter, useDocument } from '@/store/pinia/document'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ListController from '@/views/_MyPage/OwnPost/components/ListController.vue'
import PostList from '@/views/_MyPage/OwnPost/components/PostList.vue'

const mainViewName = ref('내 작성글')
const userInfo = inject<ComputedRef<User>>('userInfo')

const postFilter = ref<PostFilter>({
  user: '',
  search: '',
  ordering: '-created',
  page: 1,
})

const listFiltering = (payload: PostFilter) => {
  postFilter.value.ordering = payload.ordering
  postFilter.value.search = payload.search
  postFilter.value.page = payload.page
  fetchPostList({ ...postFilter.value })
}

const docStore = useDocument()
const postList = computed(() => docStore.postList)

const fetchPostList = (payload: PostFilter) => docStore.fetchPostList(payload)

const dataSetup = (pk: number) => {
  postFilter.value.user = pk
  fetchPostList(postFilter.value)
}

onBeforeMount(() => dataSetup(userInfo?.value.pk as number))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <div class="pt-3">
        <ListController ref="fController" :post-filter="postFilter" @list-filter="listFiltering" />

        <PostList :post-list="postList" :view-route="mainViewName" />
      </div>
    </CCardBody>
  </ContentBody>
</template>
