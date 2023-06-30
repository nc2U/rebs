<script lang="ts" setup>
import { computed, onBeforeMount, reactive, ref, watch } from 'vue'
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

const projStore = useProject()
const project = computed(() => projStore.project?.pk)
watch(project, val => {
  if (!!val) dataSet(val)
  else dataReset()
  payStore.priceList = [] // 가격 상태 초기화
})

const contStore = useContract()
const contList = computed(() => contStore.contList)
const orderGroupList = computed(() => contStore.orderGroupList)

const pDataStore = useProjectData()
const unitTypeList = computed(() => pDataStore.unitTypeList)

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

const fetchContList = (projId: number) => contStore.fetchContList(projId)
const fetchOrderGroupList = (projId: number) =>
  contStore.fetchOrderGroupList(projId)
const allContPriceSet = (payload: SimpleCont) =>
  contStore.allContPriceSet(payload)

const fetchTypeList = (projId: number) => pDataStore.fetchTypeList(projId)
const fetchFloorTypeList = (projId: number) =>
  pDataStore.fetchFloorTypeList(projId)

const payStore = usePayment()
const fetchPriceList = (queryIds: Ids) => payStore.fetchPriceList(queryIds)
const createPrice = (payload: Price) => payStore.createPrice(payload)
const updatePrice = (payload: Price) => payStore.updatePrice(payload)
const deletePrice = (payload: Ids & { pk: number }) =>
  payStore.deletePrice(payload)

// 차수 선택 시 실행 함수
const orderSelect = (order: number) => {
  order_group.value = order // order_group pk 값 할당
  priceMessage.value = !order
    ? '공급가격을 입력하기 위해 [차수 정보]를 선택하여 주십시요.'
    : '공급가격을 입력하기 위해 [타입 정보]를 선택하여 주십시요.'
  payStore.priceList = [] // 가격 상태 초기화
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

const onCreatePrice = (payload: Price) => createPrice(payload)
const onUpdatePrice = (payload: Price) => updatePrice(payload)
const onDeletePrice = (pk: number) => deletePrice({ ...{ pk }, ...queryIds })

const contPriceSet = () => {
  const cont = contList.value[0]
  allContPriceSet({ ...cont })
}

const dataSet = (pk: number) => {
  fetchContList(pk)
  fetchOrderGroupList(pk)
  fetchTypeList(pk)
  fetchFloorTypeList(pk)
}

const dataReset = () => {
  contStore.contList = []
  contStore.orderGroupList = []
  pDataStore.unitTypeList = []
  pDataStore.floorTypeList = []
}

onBeforeMount(() => dataSet(project.value || projStore.initProjId))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <PriceSelectForm
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
