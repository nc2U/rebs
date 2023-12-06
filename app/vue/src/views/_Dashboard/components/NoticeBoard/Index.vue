<script lang="ts" setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import NoticeList from './components/NoticeList.vue'
import NoticeView from './components/NoticeView.vue'
import NoticeForm from '@/views/_Dashboard/components/NoticeBoard/components/NoticeForm.vue'

const route = useRoute() as { name: string }
const msg = ref('공지 사항')

const postFilter = ref({
  ordering: '-created',
  search: '',
})
const postList = ref([])
</script>

<template>
  <CContainer fluid>
    <CCard>
      <CCardBody>
        <h5>{{ msg }}</h5>
        <hr />
        <ListController v-if="route.name === '공지 사항'" :post-filter="postFilter" />
        <CategoryTabs v-if="route.name === '공지 사항'" />
        <NoticeList v-if="route.name === '공지 사항'" :post-list="postList" />
        <NoticeView v-else-if="route.name.includes('보기')" view-route="공지 사항" :curr-page="1" />
        <NoticeForm v-else-if="route.name.includes('작성')" view-route="공지 사항" />
      </CCardBody>
    </CCard>
  </CContainer>
</template>
