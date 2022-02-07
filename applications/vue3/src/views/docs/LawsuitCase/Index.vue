<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <CompanySelect :company="company" @com-select="comSelect" />
    </CCardBody>
  </CCard>

  <component :is="compName" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import CompanySelect from '@/components/CompanySelect/Index.vue'
import BlankComponent from '@/components/BlankComponent.vue'
import HeaderMixin from '@/views/docs/_menu/headermixin'
import CompanyMixin from '@/views/settings/companyMixin'

export default defineComponent({
  name: 'LawsuitCase',
  mixins: [HeaderMixin, CompanyMixin],
  components: {
    HeaderNav,
    CompanySelect,
    BlankComponent,
  },
  data() {
    return {
      compName: 'BlankComponent',
    }
  },
})
</script>
