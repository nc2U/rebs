<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />

  <ContentBody>
    <component
      :is="compName"
      :company="company"
      :update="update"
      @to-create="toCreate"
      @to-update="toUpdate"
      @reset-form="resetForm"
      @create-form="createForm"
      @update-form="updateForm"
    />
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/settings/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import CompanyForm from './components/CompanyForm.vue'
import CompanyDetail from './components/CompanyDetail.vue'
import { mapActions, mapState } from 'vuex'

export default defineComponent({
  name: 'CompanyInfo',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    CompanyForm,
    CompanyDetail,
  },
  data() {
    return {
      compName: 'CompanyForm',
      update: false,
    }
  },
  computed: {
    ...mapState('settings', ['company']),
  },
  watch: {
    company() {
      this.compName = 'CompanyDetail'
    },
  },
  methods: {
    createForm() {
      this.update = false
      this.compName = 'CompanyForm'
    },
    updateForm() {
      this.update = true
      this.compName = 'CompanyForm'
    },
    resetForm() {
      this.update = false
      this.compName = 'CompanyDetail'
    },
    toCreate(payload: any) {
      this.createCompany(payload)
    },
    toUpdate(payload: any) {
      this.updateCompany(payload)
    },
    ...mapActions('settings', ['createCompany', 'updateCompany']),
  },
})
</script>
