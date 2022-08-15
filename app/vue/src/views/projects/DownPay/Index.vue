<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DownPayAddForm from '@/views/projects/DownPay/components/DownPayAddForm.vue'
import DownPayFormList from '@/views/projects/DownPay/components/DownPayFormList.vue'

const store = useStore()
const projectStore = useProject()

const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const orderGroupList = computed(() => store.state.contract.orderGroupList)
const unitTypeList = computed(() => store.state.project.unitTypeList)

const fetchOrderGroupList = (projId: number) =>
  store.dispatch('contract/fetchOrderGroupList', projId)

const fetchTypeList = (projId: number) =>
  store.dispatch('project/fetchTypeList', projId)

const fetchDownPayList = (payload: any) =>
  store.dispatch('payment/fetchDownPayList', payload)

const createDownPay = (payload: any) =>
  store.dispatch('payment/createDownPay', payload)

const updateDownPay = (payload: any) =>
  store.dispatch('payment/updateDownPay', payload)

const deleteDownPay = (payload: any) =>
  store.dispatch('payment/deleteDownPay', payload)

onBeforeMount(() => {
  fetchDownPayList({ project: initProjId.value })
  fetchOrderGroupList(initProjId.value)
  fetchTypeList(initProjId.value)
})

const onSelectAdd = (target: any) => {
  if (!!target) {
    fetchOrderGroupList(target)
    fetchTypeList(target)
    fetchDownPayList({ project: target })
  } else {
    store.commit('contract/updateState', { orderGroupList: [] })
    store.commit('project/updateState', { unitTypeList: [] })
    store.commit('payment/updateState', { downPayList: [] })
  }
}
const onSubmit = (payload: any) =>
  createDownPay({ ...{ project: project.value }, ...payload })

const onUpdateDownPay = (payload: any) =>
  updateDownPay({ ...{ project: project.value }, ...payload })

const onDeleteDownPay = (pk: number) =>
  deleteDownPay({ ...{ pk }, ...{ project: project.value } })
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
        @on-submit="onSubmit"
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
