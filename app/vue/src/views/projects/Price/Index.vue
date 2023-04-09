<script lang="ts" setup>
import { computed, onBeforeMount, reactive, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { usePayment } from '@/store/pinia/payment'
import { useProjectData } from '@/store/pinia/project_data'
import { OrderGroup, SimpleCont, UnitType } from '@/store/types/contract'
import { Price } from '@/store/types/payment'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PriceSelectForm from '@/views/projects/Price/components/PriceSelectForm.vue'
import PriceFormList from '@/views/projects/Price/components/PriceFormList.vue'

const order_group = ref<number | null>(null)
const unit_type = ref<number | null>(null)

type Ids = {
  project: number | null
  order_group: number | null
  unit_type: number | null
}

const queryIds = reactive<Ids>({
  project: null,
  order_group: null,
  unit_type: null,
})

const priceMessage = ref(
  '공급가격을 입력하기 위해 [차수 정보]를 선택하여 주십시요.',
)

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const contractStore = useContract()
const contList = computed(() => contractStore.contList)
const orderGroupList = computed(() => contractStore.orderGroupList)

const projectDataStore = useProjectData()
const unitTypeList = computed(() => projectDataStore.unitTypeList)

const condTexts = computed(() => {
  // 차수명과 타입명 구하기
  const orderText = orderGroupList.value
    .filter((o: OrderGroup) => o.pk == order_group.value)
    .map((o: OrderGroup) => o.order_group_name)[0]
  const typeText = unitTypeList.value
    .filter((t: UnitType) => t.pk == unit_type.value)
    .map((t: UnitType) => t.name)[0]
  return { orderText, typeText }
})

const fetchContList = (projId: number) => contractStore.fetchContList(projId)
const fetchOrderGroupList = (projId: number) =>
  contractStore.fetchOrderGroupList(projId)
const allContPriceSet = (payload: SimpleCont) =>
  contractStore.allContPriceSet(payload)

const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)
const fetchFloorTypeList = (projId: number) =>
  projectDataStore.fetchFloorTypeList(projId)

const paymentStore = usePayment()
const fetchPriceList = (queryIds: Ids) => paymentStore.fetchPriceList(queryIds)
const createPrice = (payload: Price) => paymentStore.createPrice(payload)
const updatePrice = (payload: Price) => paymentStore.updatePrice(payload)
const deletePrice = (payload: Ids & { pk: number }) =>
  paymentStore.deletePrice(payload)

const formSelect = ref()

// 프로젝트 선택 시 실행 함수
const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchContList(target)
    fetchOrderGroupList(target)
    fetchTypeList(target)
    fetchFloorTypeList(target)
    formSelect.value.orderDisabled = false
  } else {
    contractStore.contList = []
    contractStore.orderGroupList = []
    projectDataStore.unitTypeList = []
    projectDataStore.floorTypeList = []
    formSelect.value.orderDisabled = true
  }
  // 프로젝트 change 이벤트 발생 시 항상 실행
  resetPrices() // 가격 상태 초기화
}

// 차수 선택 시 실행 함수
const orderSelect = (order: number) => {
  order_group.value = order // order_group pk 값 할당
  priceMessage.value = !order
    ? '공급가격을 입력하기 위해 [차수 정보]를 선택하여 주십시요.'
    : '공급가격을 입력하기 위해 [타입 정보]를 선택하여 주십시요.'
  resetPrices() // 가격 상태 초기화
}
// 타입 선택 시 실행 함수
const typeSelect = (type: number) => {
  unit_type.value = type // unit_type pk 값 할당
  priceMessage.value = !type
    ? '공급가격을 입력하기 위해 [타입 정보]를 선택하여 주십시요.'
    : ''
  if (project.value) {
    queryIds.project = project.value
    queryIds.order_group = order_group.value
    queryIds.unit_type = unit_type.value
    fetchPriceList(queryIds) // 가격 상태 저장 실행
  }
}
// 프로젝트 또는 차수 선택 변경 시 가격 데이터 초기화
const resetPrices = () => (paymentStore.priceList = [])

const onCreatePrice = (payload: Price) => createPrice(payload)
const onUpdatePrice = (payload: Price) => updatePrice(payload)
const onDeletePrice = (pk: number) => deletePrice({ ...{ pk }, ...queryIds })

const contPriceSet = () => {
  const cont = contList.value[0]
  allContPriceSet({ ...cont })
}

onBeforeMount(() => {
  if (initProjId.value) {
    fetchContList(initProjId.value)
    fetchOrderGroupList(initProjId.value)
    fetchTypeList(initProjId.value)
    fetchFloorTypeList(initProjId.value)
  }
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
      <PriceSelectForm
        ref="formSelect"
        :project="project"
        :orders="orderGroupList"
        :types="unitTypeList"
        @on-order-select="orderSelect"
        @on-type-select="typeSelect"
        @cont-price-set="contPriceSet"
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
