<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <ProjectSelect :project="project" @proj-select="projSelect" />
      <IndexSummary :project="project" />
    </CCardBody>
  </CCard>

  <component :is="compName" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import ProjectSelect from '@/layouts/ContentHeader/ProjectSelect/Index.vue'
import IndexSummary from './components/IndexSummary.vue'
import IndexList from './components/IndexList.vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin1'
import ProjectMixin from '@/views/projects/projectMixin'

export default defineComponent({
  name: 'ContractIndex',
  mixins: [HeaderMixin, ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    IndexSummary,
    IndexList,
  },
  data() {
    return {
      compName: 'IndexList',
    }
  },
})
</script>
