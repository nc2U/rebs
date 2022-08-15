<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PayOrderAddForm from '@/views/projects/PayOrder/components/PayOrderAddForm.vue'
import PayOrderFormList from '@/views/projects/PayOrder/components/PayOrderFormList.vue'

const store = useStore()
const projectStore = useProject()

const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const fetchPayOrderList = (projId: number) =>
  store.dispatch('payment/fetchPayOrderList', projId)

const createPayOrder = (payload: any) =>
  store.dispatch('payment/createPayOrder', payload)

const updatePayOrder = (payload: any) =>
  store.dispatch('payment/updatePayOrder', payload)

const deletePayOrder = (payload: any) =>
  store.dispatch('payment/deletePayOrder', payload)

onBeforeMount(() => fetchPayOrderList(initProjId.value))

const onSelectAdd = (target: any) => {
  if (!!target) fetchPayOrderList(target)
  else store.commit('payment/updateState', { payOrderList: [] })
}
const onSubmit = (payload: any) =>
  createPayOrder({ ...{ project: project.value }, ...payload })

const onUpdatePayOrder = (payload: any) =>
  updatePayOrder({ ...{ project: project.value }, ...payload })

const onDeletePayOrder = (pk: number) =>
  deletePayOrder({ ...{ pk }, ...{ project: project.value } })
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <PayOrderAddForm :disabled="!project" @on-submit="onSubmit" />
      <PayOrderFormList
        @on-update="onUpdatePayOrder"
        @on-delete="onDeletePayOrder"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
