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

  <component
    :is="compName"
    :userInfo="userInfo"
    :company="company"
    :update="update"
    @to-create="toCreate"
    @to-update="toUpdate"
    @reset-form="resetForm"
    @create-form="createForm"
    @update-form="updateForm"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import CompanySelect from '@/layouts/ContentHeader/CompanySelect/Index.vue'
import CompanyForm from './components/CompanyForm.vue'
import CompanyDetail from './components/CompanyDetail.vue'
import { mapActions, mapState } from 'vuex'
import HeaderMixin from '@/views/settings/_menu/headermixin'
import CompanyMixin from '@/views/settings/companyMixin'

export default defineComponent({
  name: 'CompanyInfo',
  mixins: [HeaderMixin, CompanyMixin],
  components: {
    HeaderNav,
    CompanySelect,
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
    ...mapState('accounts', ['userInfo']),
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
