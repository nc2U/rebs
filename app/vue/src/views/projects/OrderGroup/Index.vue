<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { write_project } from '@/utils/pageAuth'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { type OrderGroup } from '@/store/types/contract'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import OrderAddForm from '@/views/projects/OrderGroup/components/OrderAddForm.vue'
import OrderFormList from '@/views/projects/OrderGroup/components/OrderFormList.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const contStore = useContract()

const fetchOrderGroupList = (pk: number) => contStore.fetchOrderGroupList(pk)
const createOrderGroup = (payload: OrderGroup) => contStore.createOrderGroup(payload)
const updateOrderGroup = (payload: OrderGroup) => contStore.updateOrderGroup(payload)
const deleteOrderGroup = (payload: { pk: number; project: number }) =>
  contStore.deleteOrderGroup(payload)

const onSubmit = (payload: OrderGroup) =>
  createOrderGroup({ ...{ project: project.value }, ...payload })

const onUpdateOrder = (payload: OrderGroup) =>
  updateOrderGroup({ ...{ project: project.value }, ...payload })

const onDeleteOrder = (pk: number) =>
  deleteOrderGroup({ pk, project: project.value || projStore.initProjId })

const projSelect = (target: number | null) => {
  contStore.orderGroupList = []
  if (!!target) fetchOrderGroupList(target)
}

onBeforeMount(() => fetchOrderGroupList(project.value || projStore.initProjId))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="ProjectSelect"
    @proj-select="projSelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <OrderAddForm v-if="write_project" :disabled="!project" @on-submit="onSubmit" />
      <OrderFormList @on-update="onUpdateOrder" @on-delete="onDeleteOrder" />
    </CCardBody>
  </ContentBody>
</template>
