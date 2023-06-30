<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import Multiselect from '@vueform/multiselect'

const emit = defineEmits(['proj-select'])

const projStore = useProject()
const project = computed(() => projStore.project?.pk || projStore.initProjId)
const projSelectList = computed(() => projStore.projSelect)

const projSelect = (target: number | null) => {
  if (!!target) emit('proj-select', target)
  else projStore.project = null
}

onBeforeMount(() => {
  projStore.fetchProjectList()
  projStore.fetchProject(project.value)
})
</script>

<template>
  <CRow class="m-0 align-items-center">
    <CFormLabel class="col-lg-1 col-form-label text-body">프로젝트</CFormLabel>
    <CCol md="6" lg="3">
      <Multiselect
        :value="project"
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
