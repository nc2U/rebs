<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch, Ref } from 'vue'
import { useStore } from 'vuex'
import { headerSecondary } from '@/utils/cssMixins'

defineProps({ date: { type: String, default: '' } })

const dateIncSet: Ref<Array<number> | null> = ref(null)
const dateOutSet: Ref<Array<number> | null> = ref(null)
const dateIncTotal = ref(0)
const dateOutTotal = ref(0)

const store = useStore()

const listAccD1List = computed(() => store.state.comCash.listAccD1List)
const listAccD2List = computed(() => store.state.comCash.listAccD2List)
const listAccD3List = computed(() => store.state.comCash.listAccD3List)
const comBankList = computed(() => store.state.comCash.comBankList)
const dateCashBook = computed(() => store.state.comCash.dateCashBook)

const getDAccText = (num: number, acc: any) => {
  return acc.filter((d: any) => d.pk === num).map((d: any) => d.name)[0]
}

const getBankAcc = (num: number) => {
  return comBankList.value
    .filter((b: any) => b.pk === num)
    .map((b: any) => b.alias_name)[0]
}
const setData = () => {
  dateIncSet.value = dateCashBook.value.filter(
    (i: any) => i.income > 0 && !i.outlay,
  )
  dateOutSet.value = dateCashBook.value.filter(
    (o: any) => o.outlay > 0 && !o.income,
  )
  dateIncTotal.value = dateIncSet.value
    ? dateIncSet.value
        .map((i: any) => i.income)
        .reduce((x: number, y: number) => x + y, 0)
    : null
  dateOutTotal.value = dateOutSet.value
    ? dateOutSet.value
        .map((o: any) => o.outlay)
        .reduce((x: number, y: number) => x + y, 0)
    : null
}

watch(dateCashBook, () => setData())
onBeforeMount(() => setData())
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="14%" />
      <col width="15%" />
      <col width="15%" />
      <col width="20%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="6">
          <strong>
            <CIcon name="cilFolderOpen" />
            본사 당일 입금내역
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 기준
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="headerSecondary" class="text-center">
        <CTableHeaderCell>구분</CTableHeaderCell>
        <CTableHeaderCell>계정</CTableHeaderCell>
        <CTableHeaderCell>세부 계정</CTableHeaderCell>
        <CTableHeaderCell>입금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow v-for="inc in dateIncSet" :key="inc.pk" class="text-center">
        <CTableDataCell>
          {{ getDAccText(inc.account_d1, listAccD1List) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ getDAccText(inc.account_d2, listAccD2List) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ getDAccText(inc.account_d3, listAccD3List) }}
        </CTableDataCell>
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
        <CTableDataCell></CTableDataCell>
        <CTableDataCell color="success"></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
      </CTableRow>

      <CTableRow :color="headerSecondary" class="text-right">
        <CTableHeaderCell colspan="3" class="text-center">
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
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="14%" />
      <col width="15%" />
      <col width="15%" />
      <col width="20%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="6">
          <strong>
            <CIcon name="cilFolderOpen" />
            본사 당일 출금내역
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 기준
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="headerSecondary" class="text-center">
        <CTableHeaderCell>구분</CTableHeaderCell>
        <CTableHeaderCell>계정</CTableHeaderCell>
        <CTableHeaderCell>세부 계정</CTableHeaderCell>
        <CTableHeaderCell>출금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow v-for="out in dateOutSet" :key="out.pk" class="text-center">
        <CTableDataCell>
          {{ getDAccText(out.account_d1, listAccD1List) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ getDAccText(out.account_d2, listAccD2List) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ getDAccText(out.account_d3, listAccD3List) }}
        </CTableDataCell>
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
        <CTableDataCell></CTableDataCell>
        <CTableDataCell color="danger"></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
      </CTableRow>

      <CTableRow :color="headerSecondary" class="text-right">
        <CTableHeaderCell colspan="3" class="text-center">
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
