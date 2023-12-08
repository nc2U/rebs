<script lang="ts" setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import type { Attatches, Post } from '@/store/types/document'
import NoticeList from './components/NoticeList.vue'
import NoticeView from './components/NoticeView.vue'
import NoticeForm from '@/views/_Dashboard/components/NoticeBoard/components/NoticeForm.vue'

const route = useRoute() as { name: string }
const routeName = ref('공지 사항')

const postFilter = ref({
  ordering: '-created',
  search: '',
})
const postList = ref([])

const onSubmit = (payload: Post & Attatches) => {
  console.log(payload)

  // const { pk, ...getData } = payload
  // getData.company = company.value
  // getData.newFiles = newFiles.value
  // getData.cngFiles = cngFiles.value
  //
  // const form = new FormData()
  //
  // for (const key in getData) {
  //   if (key === 'links' || key === 'files') {
  //     getData[key]?.forEach(val => form.append(key, JSON.stringify(val)))
  //   } else if (key === 'newLinks' || key === 'newFiles' || key === 'cngFiles') {
  //     if (key === 'cngFiles') {
  //       getData[key]?.forEach(val => {
  //         form.append('cngPks', val.pk as any)
  //         form.append('cngFiles', val.file as Blob)
  //       })
  //     } else getData[key]?.forEach(val => form.append(key, val as string | Blob))
  //   } else {
  //     const formValue = getData[key] === null ? '' : getData[key]
  //     form.append(key, formValue as string)
  //   }
  // }
  //
  // if (pk) {
  //   await updatePost({ pk, form })
  //   await router.replace({
  //     name: `${mainViewName.value} - 보기`,
  //     params: { postId: pk },
  //   })
  // } else {
  //   await createPost({ form })
  //   await router.replace({ name: `${mainViewName.value}` })
  //   fController.value.resetForm()
  // }
  // newFiles.value = []
  // cngFiles.value = []
}
</script>

<template>
  <CContainer fluid>
    <CCard>
      <CCardBody>
        <h5>{{ routeName }}</h5>
        <hr />
        <ListController v-if="route.name === routeName" :post-filter="postFilter" />
        <CategoryTabs v-if="route.name === routeName" />
        <NoticeList v-if="route.name === routeName" :post-list="postList" />
        <NoticeView
          v-else-if="route.name.includes('보기')"
          :view-route="routeName"
          :curr-page="1"
        />
        <NoticeForm
          v-else-if="route.name.includes('작성')"
          :view-route="routeName"
          @on-submit="onSubmit"
        />
      </CCardBody>
    </CCard>
  </CContainer>
</template>
