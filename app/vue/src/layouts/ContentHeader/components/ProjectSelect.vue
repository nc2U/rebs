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
  if (initProjId.value) projectStore.fetchProject(initProjId.value)
  projectStore.fetchProjectList()
})
</script>

<template>
  <CRow class="m-0">
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
  </CRow>
</template>
