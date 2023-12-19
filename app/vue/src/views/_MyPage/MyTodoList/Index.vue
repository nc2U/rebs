<script lang="ts" setup="">
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import TodoListApp from '@/components/TodoListApp/index.vue'
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody>
      <CRow>
        <CCol class="text-left pt-5" lg="12" xl="4">
          <TodoListApp />
        </CCol>
        <CCol lg="12" xl="4" />
        <CCol lg="12" xl="4" />
      </CRow>
    </CCardBody>
  </ContentBody>
</template>
