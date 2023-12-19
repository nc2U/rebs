<script lang="ts" setup="">
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
        <CCol class="text-left p-5">
          <TodoListApp />
        </CCol>
      </CRow>
    </CCardBody>
  </ContentBody>
</template>
