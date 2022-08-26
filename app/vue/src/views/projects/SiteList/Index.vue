<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddSite from './components/AddSite.vue'
import SiteList from './components/SiteList.vue'

const listControl = ref()

const dataFilter = ref({
  page: 1,
  from_date: '',
  to_date: '',
  sort: '',
  pro_acc_d1: '',
  pro_acc_d2: '',
  bank_account: '',
  search: '',
})

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId.toString())

const siteStore = useSite()

const onSelectAdd = (target: any) => {
  if (!!target) {
    siteStore.fetchSiteList(target)
  } else {
    siteStore.siteList = []
  }
}

const listFiltering = (payload: any) => {
  dataFilter.value = payload
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  listControl.value.listFiltering(page)
}

const onCreate = (payload: any) => {
  payload.project = project.value
  // if (payload.sort === '3' && payload.bank_account_to) {
  //   const { bank_account_to, income, ...inputData } = payload
  //   createPrCashBook(inputData)
  //
  //   delete inputData.bank_account
  //   delete inputData.outlay
  //
  //   createPrCashBook({
  //     ...{ bank_account: bank_account_to, income },
  //     ...inputData,
  //   })
  // } else createPrCashBook(payload)
}

const onUpdate = (payload: any) => 1
//   updatePrCashBook({ ...{ filters: dataFilter.value }, ...payload })

const multiSubmit = (payload: any) => {
  const { formData, sepData } = payload
  console.log(formData, sepData)
  // if (formData.sort) {
  //   if (formData.pk) onUpdate(formData)
  //   else onCreate(formData)
  // }
  // if (sepData.sort) {
  //   if (sepData.pk) onUpdate(sepData)
  //   else onCreate({ ...{ filters: dataFilter.value }, ...sepData })
  // }
}

const onDelete = (payload: any) => 1
//   deletePrCashBook({ ...{ filters: dataFilter.value }, ...payload })

onBeforeMount(() => {
  siteStore.fetchSiteList(initProjId.value)
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController />
      <AddSite />
      <SiteList
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
