<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { Project } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import IndexForm from '@/views/projects/List/components/IndexForm.vue'
import IndexDetail from '@/views/projects/List/components/IndexDetail.vue'

const compName = ref('IndexDetail')

const projectStore = useProject()

const project = computed(() => projectStore.project)

watch(project, () => (compName.value = 'IndexDetail'))

const createProject = (payload: Project) => projectStore.createProject(payload)
const updateProject = (payload: Project) => projectStore.updateProject(payload)

const createForm = () => (compName.value = 'CreateForm')
const updateForm = () => (compName.value = 'UpdateForm')
const resetForm = () => (compName.value = 'IndexDetail')

const toCreate = (payload: Project) => createProject(payload)
const toUpdate = (payload: Project) => updateProject(payload)
const toSubmit = (payload: Project) => {
  if (payload.pk) toUpdate(payload)
  else toCreate(payload)
}
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <IndexDetail
      v-if="compName === 'IndexDetail'"
      :project="project"
      @reset-form="resetForm"
      @create-form="createForm"
      @update-form="updateForm"
    />

    <IndexForm
      v-if="compName === 'CreateForm'"
      @to-submit="toSubmit"
      @reset-form="resetForm"
    />

    <IndexForm
      v-if="compName === 'UpdateForm'"
      :project="project"
      @to-submit="toSubmit"
      @reset-form="resetForm"
    />
  </ContentBody>
</template>
