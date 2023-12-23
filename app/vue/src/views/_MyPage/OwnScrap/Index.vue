<script lang="ts" setup="">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import { useRoute } from 'vue-router'
import type { User } from '@/store/types/accounts'
import { type PostFilter, useDocument } from '@/store/pinia/document'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import DocsList from '@/components/Documents/DocsList.vue'
import DocsView from '@/components/Documents/DocsView.vue'
import DocsForm from '@/components/Documents/DocsForm.vue'

const mainViewName = ref('스크랩')
const userInfo = inject<ComputedRef<User>>('userInfo')

const route = useRoute() as { name: string }

const docStore = useDocument()
const post = computed(() => docStore.post)
const postList = computed(() => docStore.postList)

const fetchPostList = (payload: PostFilter) => docStore.fetchPostList(payload)

onBeforeMount(() => fetchPostList({ user: userInfo?.value.pk }))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="route.name === mainViewName" class="pt-3">
        <DocsList :post-list="postList" :view-route="mainViewName" />
      </div>

      <div v-else-if="route.name.includes('보기')">
        <DocsView :curr-page="1" :view-route="mainViewName" />
      </div>

      <div v-else-if="route.name.includes('작성')">
        <DocsForm :view-route="mainViewName" :category-list="[]" />
      </div>

      <div v-else-if="route.name.includes('수정')">
        <DocsForm :view-route="mainViewName" :category-list="[]" />
      </div>
    </CCardBody>
  </ContentBody>
</template>
