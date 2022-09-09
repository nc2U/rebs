<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { usePayment } from '@/store/pinia/payment'
import { PayOrder } from '@/store/types/payment'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PayOrderAddForm from '@/views/projects/PayOrder/components/PayOrderAddForm.vue'
import PayOrderFormList from '@/views/projects/PayOrder/components/PayOrderFormList.vue'

const projectStore = useProject()

const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const paymentStore = usePayment()
const fetchPayOrderList = (projId: number) =>
  paymentStore.fetchPayOrderList(projId)

const createPayOrder = (payload: PayOrder) =>
  paymentStore.createPayOrder(payload)

const updatePayOrder = (payload: PayOrder) =>
  paymentStore.updatePayOrder(payload)

const deletePayOrder = (pk: number, projId: number) =>
  paymentStore.deletePayOrder(pk, projId)

onBeforeMount(() => fetchPayOrderList(initProjId.value))

const onSelectAdd = (target: number) => {
  if (!!target) fetchPayOrderList(target)
  else paymentStore.payOrderList = []
}
const onSubmit = (payload: PayOrder) =>
  createPayOrder({ ...{ project: project.value }, ...payload })

const onUpdatePayOrder = (payload: PayOrder) =>
  updatePayOrder({ ...{ project: project.value }, ...payload })

const onDeletePayOrder = (pk: number) => deletePayOrder(pk, project.value)
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
