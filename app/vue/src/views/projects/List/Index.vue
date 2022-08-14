<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import { useStore } from 'vuex'
import { useAccount } from '@/store/pinia/account'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { Project } from '@/store/pinia/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import IndexForm from '@/views/projects/List/components/IndexForm.vue'
import IndexDetail from '@/views/projects/List/components/IndexDetail.vue'

const compName = ref('IndexDetail')
const update = ref(false)

const store = useStore()
const accountStore = useAccount()
const projectStore = useProject()

const userInfo = computed(() => accountStore.userInfo)
const project = computed(() => projectStore.project)

watch(project, () => (compName.value = 'IndexDetail'))

const createProject = (payload: Project) =>
  store.dispatch('project/createProject', payload)
const updateProject = (payload: { pk: string } & Project) =>
  store.dispatch('project/updateProject', payload)

const createForm = () => {
  update.value = false
  compName.value = 'IndexForm'
}

const updateForm = () => {
  update.value = true
  compName.value = 'IndexForm'
}

const resetForm = () => {
  update.value = false
  compName.value = 'IndexDetail'
}
const toCreate = (payload: Project) => createProject(payload)
const toUpdate = (payload: { pk: string } & Project) => updateProject(payload)
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <IndexDetail
      v-if="compName === 'IndexDetail'"
      :user-info="userInfo"
      :project="project"
      :update="update"
      @to-create="toCreate"
      @to-update="toUpdate"
      @reset-form="resetForm"
      @create-form="createForm"
      @update-form="updateForm"
    />

    <IndexForm v-if="compName === 'IndexForm'" />
  </ContentBody>
</template>
