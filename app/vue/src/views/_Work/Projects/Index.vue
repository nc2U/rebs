<script setup lang="ts">
import { computed, ref } from 'vue'
import { pageTitle, navMenu1, navMenu2 } from '@/views/_Work/_menu/headermixin1'
import { useRoute } from 'vue-router'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import ProjectList from '@/views/_Work/Projects/components/ProjectList.vue'
import ProjectForm from '@/views/_Work/Projects/components/ProjectForm.vue'

const cBody = ref()

const route = useRoute()
const navMenu = computed(() => (route.params['projId'] ? navMenu2 : navMenu1))

const sideNavCAll = () => cBody.value.toggle()
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <ProjectList v-if="route.name === '프로젝트'" />

      <ProjectForm v-if="route.name === '프로젝트 - 생성'" />
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
