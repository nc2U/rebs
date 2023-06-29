<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { useContract } from '@/store/pinia/contract'
import { usePayment } from '@/store/pinia/payment'
import { DownPay } from '@/store/types/payment'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DownPayAddForm from '@/views/projects/DownPay/components/DownPayAddForm.vue'
import DownPayFormList from '@/views/projects/DownPay/components/DownPayFormList.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk || projStore.initProjId)

const contStore = useContract()
const orderGroupList = computed(() => contStore.orderGroupList)

const pDataStore = useProjectData()
const unitTypeList = computed(() => pDataStore.unitTypeList)

const fetchOrderGroupList = (projId: number) =>
  contStore.fetchOrderGroupList(projId)

const fetchTypeList = (projId: number) => pDataStore.fetchTypeList(projId)

const payStore = usePayment()
const fetchDownPayList = (payload: {
  project: number
  order_group?: number
  unit_type?: number
}) => payStore.fetchDownPayList(payload)
const createDownPay = (payload: DownPay) => payStore.createDownPay(payload)
const updateDownPay = (payload: DownPay) => payStore.updateDownPay(payload)
const deleteDownPay = (pk: number, projId: number) =>
  payStore.deleteDownPay(pk, projId)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchOrderGroupList(target)
    fetchTypeList(target)
    fetchDownPayList({ project: target })
  } else {
    contStore.orderGroupList = []
    pDataStore.unitTypeList = []
    payStore.downPayList = []
  }
}

const onCreateDownPay = (payload: DownPay) =>
  createDownPay({ ...{ project: project.value }, ...payload })

const onUpdateDownPay = (payload: DownPay) =>
  updateDownPay({ ...{ project: project.value }, ...payload })

const onDeleteDownPay = (pk: number) => {
  if (project.value) deleteDownPay(pk, project.value)
}

onBeforeMount(() => {
  const projectPk = project.value
  fetchDownPayList({ project: projectPk })
  fetchOrderGroupList(projectPk)
  fetchTypeList(projectPk)
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
      <DownPayAddForm
        :disabled="!project"
        :orders="orderGroupList"
        :types="unitTypeList"
        @on-submit="onCreateDownPay"
      />
      <DownPayFormList
        :orders="orderGroupList"
        :types="unitTypeList"
        @on-update="onUpdateDownPay"
        @on-delete="onDeleteDownPay"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
