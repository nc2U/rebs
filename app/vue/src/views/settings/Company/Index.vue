<script lang="ts" setup>
import { computed, ref, shallowRef, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { useStore } from 'vuex'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import CompanyForm from './components/CompanyForm.vue'
import CompanyDetail from './components/CompanyDetail.vue'

const update = ref(false)

const compName = shallowRef('CompanyDetail')

const store = useStore()

const company = computed(() => store.state.settings.company)

watch(company, () => (compName.value = 'CompanyDetail'))

const createCompany = (payload: any) =>
  store.dispatch('settings/createCompany', payload)

const updateCompany = (payload: any) =>
  store.dispatch('settings/updateCompany', payload)

const createForm = () => {
  update.value = false
  compName.value = 'CompanyForm'
}

const updateForm = () => {
  update.value = true
  compName.value = 'CompanyForm'
}

const resetForm = () => {
  update.value = false
  compName.value = 'CompanyDetail'
}

const toCreate = (payload: any) => {
  createCompany(payload)
}

const toUpdate = (payload: any) => {
  updateCompany(payload)
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CompanyDetail
      v-if="compName == 'CompanyDetail'"
      :company="company"
      :update="update"
      @to-create="toCreate"
      @to-update="toUpdate"
      @reset-form="resetForm"
      @create-form="createForm"
      @update-form="updateForm"
    />
    <CompanyForm
      v-if="compName == 'CompanyForm'"
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
