<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1">본사 문서관리</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="['본사 일반문서']" />

      <CompanySelect :company="company" @on-change="onChange" />
    </CCardBody>
  </CCard>

  <component :is="compName" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import CompanySelect from '@/components/CompanySelect/Index.vue'
import BlankComponent from '@/components/BlankComponent.vue'
import CompanyMixin from '@/views/settings/companyMixin'

export default defineComponent({
  name: 'GeneralDocs',
  mixins: [CompanyMixin],
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
