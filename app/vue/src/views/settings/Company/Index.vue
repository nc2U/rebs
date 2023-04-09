<script lang="ts" setup>
import { computed, ref, watch, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { Company } from '@/store/types/settings'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import CompanyForm from './components/CompanyForm.vue'
import CompanyDetail from './components/CompanyDetail.vue'

const compName = ref('CompanyDetail')

const companyStore = useCompany()
const company = computed(() => companyStore.company)

watch(company, () => (compName.value = 'CompanyDetail'))

const createCompany = (payload: Company) => companyStore.createCompany(payload)
const updateCompany = (payload: Company) => companyStore.updateCompany(payload)

const createForm = () => (compName.value = 'CreateForm')
const updateForm = () => (compName.value = 'UpdateForm')
const resetForm = () => (compName.value = 'CompanyDetail')

const onCreate = (payload: Company) => createCompany(payload)
const onUpdate = (payload: Company) => updateCompany(payload)

const onSubmit = (payload: Company) => {
  if (payload.pk) onUpdate(payload)
  else onCreate(payload)
}

onMounted(() => {
  if (companyStore.companyList.length === 0) createForm()
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />

  <ContentBody>
    <CompanyDetail
      v-if="compName === 'CompanyDetail'"
      :company="company"
      @create-form="createForm"
      @update-form="updateForm"
    />

    <CompanyForm
      v-if="compName === 'CreateForm'"
      @on-submit="onSubmit"
      @reset-form="resetForm"
    />

    <CompanyForm
      v-if="compName === 'UpdateForm'"
      :company="company"
      @on-submit="onSubmit"
      @reset-form="resetForm"
    />
  </ContentBody>
</template>
