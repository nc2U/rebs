<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />
      <CompanySelect :company="company" @on-change="onChange" />
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
import CompanySelect from '@/components/CompanySelect/Index.vue'
import CompanyForm from './components/CompanyForm.vue'
import CompanyDetail from './components/CompanyDetail.vue'
import { mapActions, mapGetters, mapState } from 'vuex'
import HeaderMixin from '@/views/settings/_menu/headermixin'

export default defineComponent({
  name: 'CompanyInfo',
  mixins: [HeaderMixin],
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
  created() {
    this.fetchCompany(this.initComId)
  },
  computed: {
    ...mapState('settings', ['company']),
    ...mapState('accounts', ['userInfo']),
    ...mapGetters('accounts', ['initComId']),
  },
  watch: {
    company() {
      this.compName = 'CompanyDetail'
    },
  },
  methods: {
    onChange(event: any) {
      this.fetchCompany(event.target.value)
    },
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
    async toCreate(payload: any) {
      await this.createCompany(payload)
    },
    async toUpdate(payload: any) {
      await this.updateCompany(payload)
    },
    ...mapActions('settings', [
      'fetchCompany',
      'createCompany',
      'updateCompany',
    ]),
  },
})
</script>
