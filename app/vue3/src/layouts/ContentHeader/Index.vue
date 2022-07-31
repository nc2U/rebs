<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <component
        :is="selector"
        :company="company"
        :project="project"
        @com-select="comSelect"
        @proj-select="projSelect"
      />

      <slot />
    </CCardBody>
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import CompanyMixin from '@/views/settings/companyMixin'
import ProjectMixin from '@/views/projects/projectMixin'
import CompanySelect from '@/layouts/ContentHeader/CompanySelect/Index.vue'
import ProjectSelect from '@/layouts/ContentHeader/ProjectSelect/Index.vue'

export default defineComponent({
  name: 'ContentHeader',
  mixins: [CompanyMixin, ProjectMixin],
  components: { HeaderNav, CompanySelect, ProjectSelect },
  props: {
    pageTitle: {
      type: String,
      default: 'Page Title',
    },
    navMenu: {
      type: Object,
    },
    selector: {
      type: String,
      default: 'ProjectSelect',
    },
  },
})
</script>
