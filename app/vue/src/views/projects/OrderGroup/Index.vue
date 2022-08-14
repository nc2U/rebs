<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import OrderAddForm from '@/views/projects/OrderGroup/components/OrderAddForm.vue'
import OrderFormList from '@/views/projects/OrderGroup/components/OrderFormList.vue'

const store = useStore()
const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const onSelectAdd = (target: any) => {
  if (target !== '') fetchOrderGroupList(target)
  else store.commit('contract/updateState', { orderGroupList: [] })
}

const fetchOrderGroupList = (pk: number) =>
  store.dispatch('contract/fetchOrderGroupList', pk)
const createOrderGroup = (payload: any) =>
  store.dispatch('contract/createOrderGroup', payload)
const updateOrderGroup = (payload: any) =>
  store.dispatch('contract/updateOrderGroup', payload)
const deleteOrderGroup = (payload: any) =>
  store.dispatch('contract/deleteOrderGroup', payload)

const onSubmit = (payload: any) =>
  createOrderGroup({ ...{ project: project.value }, ...payload })

const onUpdateOrder = (payload: any) =>
  updateOrderGroup({ ...{ project: project.value }, ...payload })

const onDeleteOrder = (pk: number) =>
  deleteOrderGroup({ ...{ pk }, ...{ project: project.value } })

onBeforeMount(() => {
  fetchOrderGroupList(initProjId.value)
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
      <OrderAddForm :disabled="!project" @on-submit="onSubmit" />
      <OrderFormList @on-update="onUpdateOrder" @on-delete="onDeleteOrder" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
