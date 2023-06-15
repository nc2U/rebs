<script lang="ts" setup>
import { ref, computed, onBeforeMount, nextTick, watch } from 'vue'
import { useProject } from '@/store/pinia/project'
import Multiselect from '@vueform/multiselect'

const emit = defineEmits(['proj-select'])

const currentProject = ref()

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)
const projSelectList = computed(() => projectStore.projSelect)

watch(project, val => (currentProject.value = val))

const projSelect = () =>
  nextTick(() => emit('proj-select', currentProject.value))

onBeforeMount(() => {
  currentProject.value = project.value ? project.value : initProjId.value
  projectStore.fetchProjectList()
  if (!project.value) projectStore.fetchProject(initProjId.value)
})
</script>

<template>
  <CRow class="m-0 align-items-center">
    <CFormLabel class="col-lg-1 col-form-label text-body">프로젝트</CFormLabel>
    <CCol md="6" lg="3">
      <Multiselect
        v-model="currentProject"
        :options="projSelectList"
        placeholder="프로젝트선택"
        autocomplete="label"
        :classes="{ search: 'form-control multiselect-search' }"
        :add-option-on="['enter' | 'tab']"
        searchable
        @change="projSelect"
      />
    </CCol>
    <CCol v-if="projSelectList.length === 0" class="pl-0 align-middle">
      <v-icon
        icon="mdi mdi-plus-thick"
        color="success"
        @click="$router.push({ name: '프로젝트 등록' })"
      />
    </CCol>
  </CRow>
</template>
