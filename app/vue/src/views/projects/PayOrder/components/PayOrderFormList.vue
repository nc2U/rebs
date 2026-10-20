<script lang="ts" setup>
import { computed } from 'vue'
import { usePayment } from '@/store/pinia/payment'
import { TableSecondary } from '@/utils/cssMixins'
import { usePerms } from '@/composables/usePerms'
import type { PayOrder } from '@/store/types/payment'
import PayOrderRow from '@/views/projects/PayOrder/components/PayOrder.vue'

const emit = defineEmits<{
  (e: 'on-update', payload: PayOrder): void
  (e: 'on-delete', pk: number): void
}>()

const { can, PERM } = usePerms()
const canProjectUpdate = computed(() => can(PERM.PROJECT_UPDATE))

const paymentStore = usePayment()
const payOrderList = computed(() => paymentStore.payOrderList)

const onUpdatePayOrder = (payload: PayOrder) => emit('on-update', payload)
const onDeletePayOrder = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col style="width: 8%" />
      <col style="width: 8%" />
      <col style="width: 9%" />
      <col style="width: 7%" />
      <col style="width: 7%" />
      <col style="width: 7%" />
      <col style="width: 9%" />
      <col style="width: 8%" />
      <col style="width: 9%" />
      <col style="width: 8%" />
      <col style="width: 8%" />
      <col v-if="canProjectUpdate" style="width: 12%" />
    </colgroup>
    <CTableHead :color="TableSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>타입종류</CTableHeaderCell>
        <CTableHeaderCell>회차종류</CTableHeaderCell>
        <CTableHeaderCell>계약금 산정방법</CTableHeaderCell>
        <CTableHeaderCell>공급가 포함 여부</CTableHeaderCell>
        <CTableHeaderCell class="cursor-help">
          회차코드
          <v-icon icon="mdi-tooltip-question-outline" size="14" color="grey" />
          <v-tooltip activator="parent" location="top">
            프로젝트 내 납부회차별 코드번호 - 동일 회차 중복(분리) 등록 가능
          </v-tooltip>
        </CTableHeaderCell>
        <CTableHeaderCell class="cursor-help">
          납부순서
          <v-icon icon="mdi-tooltip-question-outline" size="14" color="grey" />
          <v-tooltip activator="parent" location="top">
            동일 납부회차에 2가지 항목을 별도로 납부하여야 하는 경우(ex: 분담금 + 업무대행료) 하나의
            납입회차 코드(ex: 1)에 2개의 납부순서(ex: 1, 2)를 등록한다.
          </v-tooltip>
        </CTableHeaderCell>
        <CTableHeaderCell>회차 명</CTableHeaderCell>
        <CTableHeaderCell>별칭</CTableHeaderCell>
        <CTableHeaderCell class="cursor-help">
          약정금액
          <v-icon icon="mdi-tooltip-question-outline" size="14" color="grey" />
          <v-tooltip activator="parent" location="top">
            약정금이 차수, 타입에 관계 없이 정액인 경우 설정(예: 세대별 업무대행비)
          </v-tooltip>
        </CTableHeaderCell>
        <CTableHeaderCell class="cursor-help">
          납부비율(%)
          <v-icon icon="mdi-tooltip-question-outline" size="14" color="grey" />
          <v-tooltip activator="parent" location="top">
            분양가 대비 납부비율, 계약금 항목인 경우 "계약 금액 등록" 데이터 우선, 잔금 항목인 경우
            "공급 가격 등록" 데이터와 비교 차액 데이터 우선
          </v-tooltip>
        </CTableHeaderCell>
        <CTableHeaderCell class="text-center">설정 확장</CTableHeaderCell>
        <CTableHeaderCell v-if="canProjectUpdate">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="payOrderList.length > 0">
      <PayOrderRow
        v-for="payOrder in payOrderList"
        :key="payOrder.pk as number"
        :pay-order="payOrder"
        @on-update="onUpdatePayOrder"
        @on-delete="onDeletePayOrder"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell :colspan="canProjectUpdate ? 12 : 11" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
