<script lang="ts" setup>
import { computed, onBeforeMount, reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PriceSelectForm from '@/views/projects/Price/components/PriceSelectForm.vue'
import PriceFormList from '@/views/projects/Price/components/PriceFormList.vue'

const order_group = ref('')
const unit_type = ref('')
const queryIds = reactive({
  project: '',
  order_group: '',
  unit_type: '',
})

const priceMessage = ref(
  '공급가격을 입력하기 위해 [차수 정보]를 선택하여 주십시요.',
)

const store = useStore()
const projectStore = useProject()

const project = computed(() => projectStore.project?.pk.toString())
const initProjId = computed(() => projectStore.initProjId)
const orderGroupList = computed(() => store.state.contract.orderGroupList)
const unitTypeList = computed(() => store.state.project.unitTypeList)
const floorTypeList = computed(() => store.state.project.floorTypeList)

const condTexts = computed(() => {
  // 차수명과 타입명 구하기
  const orderText = orderGroupList.value
    .filter((o: any) => o.pk == order_group.value)
    .map((o: any) => o.order_group_name)[0]
  const typeText = unitTypeList.value
    .filter((t: any) => t.pk == unit_type.value)
    .map((t: any) => t.name)[0]
  return { orderText, typeText }
})

const fetchOrderGroupList = (projId: number) =>
  store.dispatch('contract/fetchOrderGroupList', projId)
const fetchTypeList = (projId: number) =>
  store.dispatch('project/fetchTypeList', projId)
const fetchFloorTypeList = (projId: number) =>
  store.dispatch('project/fetchFloorTypeList', projId)

const fetchPriceList = (queryIds: any) =>
  store.dispatch('payment/fetchPriceList', queryIds)
const createPrice = (payload: any) =>
  store.dispatch('payment/createPrice', payload)
const updatePrice = (payload: any) =>
  store.dispatch('payment/updatePrice', payload)
const deletePrice = (payload: any) =>
  store.dispatch('payment/deletePrice', payload)

onBeforeMount(() => {
  fetchOrderGroupList(initProjId.value)
  fetchTypeList(initProjId.value)
  fetchFloorTypeList(initProjId.value)
})

const formSelect = ref()

// 프로젝트 선택 시 실행 함수
const onSelectAdd = (target: any) => {
  if (!!target) {
    console.log(formSelect.value)
    fetchOrderGroupList(target)
    fetchTypeList(target)
    fetchFloorTypeList(target)
    formSelect.value.orderDisabled = false
  } else {
    store.commit('contract/updateState', { orderGroupList: [] })
    store.commit('project/updateState', { unitTypeList: [], floorTypeList: [] })
    formSelect.value.orderDisabled = true
  }
  // 프로젝트 change 이벤트 발생 시 항상 실행
  resetPrices() // 가격 상태 초기화
}

// 차수 선택 시 실행 함수
const orderSelect = (payload: any) => {
  order_group.value = payload // order_group pk 값 할당
  priceMessage.value =
    payload == ''
      ? '공급가격을 입력하기 위해 [차수 정보]를 선택하여 주십시요.'
      : '공급가격을 입력하기 위해 [타입 정보]를 선택하여 주십시요.'
  resetPrices() // 가격 상태 초기화
}
// 타입 선택 시 실행 함수
const typeSelect = (payload: any) => {
  unit_type.value = payload // unit_type pk 값 할당
  priceMessage.value =
    payload == ''
      ? '공급가격을 입력하기 위해 [타입 정보]를 선택하여 주십시요.'
      : ''
  queryIds.order_group = order_group.value
  queryIds.unit_type = unit_type.value
  queryIds.project = project.value || initProjId.value.toString()
  fetchPriceList(queryIds) // 갸격 상태 저장 실행
}
// 프로젝트 또는 차수 선택 변경 시 가격 데이터 초기화
const resetPrices = () => store.commit('payment/updateState', { priceList: [] })

const onCreatePrice = (payload: any) => createPrice(payload)
const onUpdatePrice = (payload: any) => updatePrice(payload)
const onDeletePrice = (pk: any) => deletePrice({ pk, ...queryIds })
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <PriceSelectForm
        ref="formSelect"
        :orders="orderGroupList"
        :types="unitTypeList"
        @on-order-select="orderSelect"
        @on-type-select="typeSelect"
      />
      <PriceFormList
        :msg="priceMessage"
        :cond-texts="condTexts"
        :query-ids="queryIds"
        @on-create="onCreatePrice"
        @on-update="onUpdatePrice"
        @on-delete="onDeletePrice"
      />
    </CCardBody>
    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
