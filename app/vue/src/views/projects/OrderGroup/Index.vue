<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { OrderGroup } from '@/store/types/contract'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import OrderAddForm from '@/views/projects/OrderGroup/components/OrderAddForm.vue'
import OrderFormList from '@/views/projects/OrderGroup/components/OrderFormList.vue'

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)

const contractStore = useContract()
const onSelectAdd = (target: number) => {
  if (!!target) fetchOrderGroupList(target)
  else contractStore.orderGroupList = []
}

const fetchOrderGroupList = (pk: number) =>
  contractStore.fetchOrderGroupList(pk)
const createOrderGroup = (payload: OrderGroup) =>
  contractStore.createOrderGroup(payload)
const updateOrderGroup = (payload: OrderGroup) =>
  contractStore.updateOrderGroup(payload)
const deleteOrderGroup = (payload: { pk: number; project: number }) =>
  contractStore.deleteOrderGroup(payload)

const onSubmit = (payload: OrderGroup) =>
  createOrderGroup({ ...{ project: project.value }, ...payload })

const onUpdateOrder = (payload: OrderGroup) =>
  updateOrderGroup({ ...{ project: project.value }, ...payload })

const onDeleteOrder = (pk: number) =>
  deleteOrderGroup({ pk, project: project.value })

onBeforeMount(() => {
  if (project.value) fetchOrderGroupList(project.value)
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
