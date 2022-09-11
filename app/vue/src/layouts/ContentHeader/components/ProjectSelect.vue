<script lang="ts" setup>
import { ref, computed, onBeforeMount, nextTick, watch } from 'vue'
import { useProject } from '@/store/pinia/project'

const emit = defineEmits(['proj-select'])

const currentProject = ref()

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk)
const projSelectList = computed(() => projectStore.projSelect)

watch(project, val => (currentProject.value = val))

const projSelect = (event: Event) =>
  nextTick(() => emit('proj-select', (event.target as HTMLSelectElement).value))

onBeforeMount(() => {
  projectStore.fetchProjectList()
  currentProject.value = initProjId.value
  projectStore.fetchProject(currentProject.value)
})
</script>

<template>
  <CRow class="m-0">
    <CFormLabel class="col-lg-1 col-form-label text-body">프로젝트</CFormLabel>
    <CCol md="6" lg="3">
      <CFormSelect v-model="currentProject" @change="projSelect">
        <option value="">프로젝트선택</option>
        <option v-for="p in projSelectList" :key="p.value" :value="p.value">
          {{ p.text }}
        </option>
      </CFormSelect>
    </CCol>
  </CRow>
</template>
