<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> 현장 문서관리</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="['현장 일반문서']" />

      <ProjectSelect :project="project" @proj-select="projSelect" />
    </CCardBody>
  </CCard>

  <component :is="compName" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import ProjectSelect from '@/layouts/ContentHeader/ProjectSelect/Index.vue'
import BlankComponent from '@/components/BlankComponent.vue'
import ProjectMixin from '@/views/projects/projectMixin'

export default defineComponent({
  name: 'ProjectGeneralDocs',
  mixins: [ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    BlankComponent,
  },
  data() {
    return {
      compName: 'BlankComponent',
    }
  },
})
</script>
