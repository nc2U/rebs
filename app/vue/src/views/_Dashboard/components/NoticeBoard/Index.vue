<script lang="ts" setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
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
        <NoticeForm v-else-if="route.name.includes('작성')" :view-route="routeName" />
      </CCardBody>
    </CCard>
  </CContainer>
</template>
