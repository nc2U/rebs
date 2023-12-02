<script lang="ts" setup>
import { ref } from 'vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import NoticeList from './components/NoticeList.vue'
import NoticeView from './components/NoticeView.vue'

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
        <ListController :post-filter="postFilter" />
        <CategoryTabs />
        <NoticeList :post-list="postList" />
      </CCardBody>
    </CCard>
  </CContainer>
</template>
