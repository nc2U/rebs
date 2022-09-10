<script lang="ts" setup>
import { useProject } from '@/store/pinia/project'
import { useCompany } from '@/store/pinia/company'
import HeaderNav from '@/components/HeaderNav.vue'
import CompanySelect from '@/layouts/ContentHeader/components/CompanySelect.vue'
import ProjectSelect from '@/layouts/ContentHeader/components/ProjectSelect.vue'

defineProps({
  pageTitle: {
    type: String,
    default: 'Page Title',
  },
  navMenu: {
    type: Array,
    default: () => ['Base Menu'],
  },
  selector: {
    type: String,
    default: 'ProjectSelect',
  },
})
const emit = defineEmits(['header-select'])

const companyStore = useCompany()
const projectStore = useProject()

const comSelect = (com: number) => {
  if (!!com) companyStore.fetchCompany(com)
  else companyStore.company = null
  emit('header-select', com)
}

const projSelect = (proj: number) => {
  if (!!proj) projectStore.fetchProject(proj)
  else projectStore.project = null
  emit('header-select', proj)
}
</script>

<template>
  <CCard class="mb-4 text-body">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <CompanySelect
        v-if="selector === 'CompanySelect'"
        @com-select="comSelect"
      />

      <ProjectSelect
        v-if="selector === 'ProjectSelect'"
        @proj-select="projSelect"
      />

      <slot />
    </CCardBody>
  </CCard>
</template>
