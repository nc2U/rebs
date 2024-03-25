<script setup lang="ts">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { navMenu2 as navMenu } from '@/views/_Work/_menu/headermixin1'
import type { Company } from '@/store/types/settings'
import { useRouter } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import IssueList from './components/IssueList.vue'
import IssueForm from '@/views/_Work/Manages/Issues/components/IssueForm.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const sideNavCAll = () => cBody.value.toggle()

const workStore = useWork()
const issueList = computed(() => workStore.issueList)
const issueProjects = computed(() => workStore.AllIssueProjects)

const router = useRouter()

const onSubmit = (payload: any) => {
  console.log(payload)
  alert('issue create!')
  router.replace({ name: '업무' })
}

onBeforeMount(() => {
  workStore.fetchIssueProjectList()
  workStore.fetchIssueList()
})
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <IssueList v-if="$route.name === '업무'" :issue-list="issueList" />

      <CRow v-if="$route.name === '업무 - 추가'" class="py-2">
        <CCol>
          <h5>새 업무만들기</h5>
        </CCol>

        <IssueForm
          :issue-projects="issueProjects"
          @on-submit="onSubmit"
          @close-form="router.push({ name: '업무' })"
        />
      </CRow>
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
