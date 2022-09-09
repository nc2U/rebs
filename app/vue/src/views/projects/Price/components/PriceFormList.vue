<script lang="ts" setup>
import { computed } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import { usePayment } from '@/store/pinia/payment'
import { Price as P } from '@/store/types/payment'
import Price from '@/views/projects/Price/components/Price.vue'
import { headerSecondary } from '@/utils/cssMixins'

const props = defineProps({
  msg: { type: String, default: '' },
  condTexts: { type: Object, default: null },
  queryIds: { type: Object, default: null },
})
const emit = defineEmits(['on-create', 'on-update', 'on-delete'])

const projectDataStore = useProjectData()
const floorTypeList = computed(() => projectDataStore.floorTypeList)

const paymentStore = usePayment()
const priceList = computed(() => paymentStore.priceList)

const getPrice = (floor: number) =>
  priceList.value.filter((p: P) => p.unit_floor_type === floor)[0]

const onCreate = (payload: P) => emit('on-create', payload)
const onUpdate = (payload: P) => emit('on-update', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col width="13%" />
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="13%" />
      <col width="13" />
    </colgroup>
    <CTableHead :color="headerSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>차수</CTableHeaderCell>
        <CTableHeaderCell>타입</CTableHeaderCell>
        <CTableHeaderCell>층별 조건</CTableHeaderCell>
        <CTableHeaderCell>건물가(단위:원)</CTableHeaderCell>
        <CTableHeaderCell>대지가(단위:원)</CTableHeaderCell>
        <CTableHeaderCell>부가세(단위:원)</CTableHeaderCell>
        <CTableHeaderCell>분양가격(단위:원)</CTableHeaderCell>
        <CTableHeaderCell>비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="!msg">
      <Price
        v-for="floor in floorTypeList"
        :key="floor.pk"
        :cond-texts="condTexts"
        :query-ids="queryIds"
        :floor="floor"
        :price="getPrice(floor.pk)"
        @on-create="onCreate"
        @on-update="onUpdate"
        @on-delete="onDelete"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell :colspan="8" class="text-center p-5 text-info">
          {{ msg }}
        </CTableDataCell>
      </CTableRow>
    </CTableBody>

    <CTableBody v-if="!msg && floorTypeList.length === 0">
      <CTableRow>
        <CTableDataCell :colspan="8" class="text-center p-5 text-danger">
          <p>
            <CIcon name="cilWarning" />
            등록된 [층별조건] 데이터가 없습니다!
          </p>
          <p>먼저 [층별조건]을 등록한 후 진행하세요.</p>
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
