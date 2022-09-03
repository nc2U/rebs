<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { useStore } from 'vuex'
import { numFormat, dateFormat } from '@/utils/baseMixins'
import { headerSecondary } from '@/utils/cssMixins'

defineProps({ date: { type: String, default: '' } })

const dateIncSet = ref([])
const dateOutSet = ref([])
const dateIncTotal = ref(0)
const dateOutTotal = ref(0)

const store = useStore()

const allAccD1List = computed(() => store.state.proCash.allAccD1List)
const allAccD2List = computed(() => store.state.proCash.allAccD2List)
const proBankAccountList = computed(
  () => store.state.proCash.proBankAccountList,
)
const proDateCashBook = computed(() => store.state.proCash.proDateCashBook)

watch(proDateCashBook, () => setData())

onBeforeMount(() => setData())

const getD1Text = (num: number) =>
  allAccD1List.value.filter((d: any) => d.pk === num).map((d: any) => d.name)[0]

const getD2Text = (num: number) =>
  allAccD2List.value.filter((d: any) => d.pk === num).map((d: any) => d.name)[0]

const getBankAcc = (num: number) =>
  proBankAccountList.value
    .filter((b: any) => b.pk === num)
    .map((b: any) => b.alias_name)[0]

const setData = () => {
  dateIncSet.value = proDateCashBook.value.filter(
    (i: any) => i.income > 0 && !i.outlay,
  )
  dateOutSet.value = proDateCashBook.value.filter(
    (o: any) => o.outlay > 0 && !o.income,
  )
  dateIncTotal.value = dateIncSet.value
    .map((i: any) => i.income)
    .reduce((x: number, y: number) => x + y, 0)
  dateOutTotal.value = dateOutSet.value
    .map((o: any) => o.outlay)
    .reduce((x: number, y: number) => x + y, 0)
}
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="25%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="5">
          <strong>
            <CIcon name="cilFolderOpen" />
            프로젝트 당일 입금내역
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 기준
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="headerSecondary" class="text-center">
        <CTableHeaderCell>항목</CTableHeaderCell>
        <CTableHeaderCell>세부 항목</CTableHeaderCell>
        <CTableHeaderCell>입금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow v-for="inc in dateIncSet" :key="inc.pk" class="text-center">
        <CTableDataCell>{{ getD1Text(inc.project_account_d1) }}</CTableDataCell>
        <CTableDataCell>{{ getD2Text(inc.project_account_d2) }}</CTableDataCell>
        <CTableDataCell class="text-right" color="success">
          {{ numFormat(inc.income) }}
        </CTableDataCell>
        <CTableDataCell>{{ getBankAcc(inc.bank_account) }}</CTableDataCell>
        <CTableDataCell class="text-left">{{ inc.trader }}</CTableDataCell>
        <CTableDataCell class="text-left">{{ inc.content }}</CTableDataCell>
      </CTableRow>

      <CTableRow class="text-center">
        <CTableDataCell>&nbsp;</CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell color="success"></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
      </CTableRow>

      <CTableRow :color="headerSecondary" class="text-right">
        <CTableHeaderCell colspan="2" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(dateIncTotal) }}</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>

  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="25%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="5">
          <strong>
            <CIcon name="cilFolderOpen" />
            프로젝트 당일 출금내역
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 기준
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="headerSecondary" class="text-center">
        <CTableHeaderCell>항목</CTableHeaderCell>
        <CTableHeaderCell>세부 항목</CTableHeaderCell>
        <CTableHeaderCell>출금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow v-for="out in dateOutSet" :key="out.pk" class="text-center">
        <CTableDataCell>{{ getD1Text(out.project_account_d1) }}</CTableDataCell>
        <CTableDataCell>{{ getD2Text(out.project_account_d2) }}</CTableDataCell>
        <CTableDataCell class="text-right" color="danger">
          {{ numFormat(out.outlay) }}
        </CTableDataCell>
        <CTableDataCell>{{ getBankAcc(out.bank_account) }}</CTableDataCell>
        <CTableDataCell class="text-left">{{ out.trader }}</CTableDataCell>
        <CTableDataCell class="text-left">{{ out.content }}</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-center">
        <CTableDataCell>&nbsp;</CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell color="danger"></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
      </CTableRow>

      <CTableRow :color="headerSecondary" class="text-right">
        <CTableHeaderCell colspan="2" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(dateOutTotal) }}</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
