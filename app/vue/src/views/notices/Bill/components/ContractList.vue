<script lang="ts" setup>
import { computed, ref, nextTick } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { TableSecondary } from '@/utils/cssMixins'
import Contract from '@/views/notices/Bill/components/Contract.vue'
import Pagination from '@/components/Pagination'

defineProps({ nowOrder: { type: Number, default: null } })
const emit = defineEmits(['page-select', 'on-ctor-chk', 'all-un-checked'])

const page = ref(1)
const allChecked = ref(false)

const contractStore = useContract()
const contractList = computed(() => contractStore.contractList)
const contractPages = computed(() => contractStore.contractPages)

const pageSelect = (page: number) => {
  allChecked.value = false
  emit('page-select', page)
}

const allUnChecked = () =>
  nextTick(() => {
    if (!allChecked.value) {
      emit('all-un-checked')
    }
  })

const onCtorChk = (payload: { chk: boolean; pk: number }) =>
  emit('on-ctor-chk', payload)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="8%" />
      <col width="10%" />
      <col width="7%" />
      <col width="12%" />
      <col width="11%" />
      <col width="8%" />
      <col width="12%" />
      <col width="20%" />
      <col width="12%" />
    </colgroup>

    <CTableHead :color="TableSecondary">
      <CTableRow class="text-center">
        <CTableHeaderCell scope="col">
          <CFormCheck
            id="checkAll"
            v-model="allChecked"
            label="전체"
            @change="allUnChecked"
          />
        </CTableHeaderCell>
        <CTableHeaderCell scope="col">차수</CTableHeaderCell>
        <CTableHeaderCell scope="col">타입</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약 일련번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">동호수</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약자</CTableHeaderCell>
        <CTableHeaderCell scope="col">납입금액합계</CTableHeaderCell>
        <CTableHeaderCell scope="col">납입상태 (완납회차)</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약일자</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Contract
        v-for="contract in contractList"
        :key="contract.pk"
        :page="page"
        :now-order="nowOrder"
        :all-checked="allChecked"
        :contract="contract"
        @on-ctor-chk="onCtorChk"
      />
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="contractPages(10)"
    class="mt-3"
    @on-ctor-pk="ctorChk"
    @active-page-change="pageSelect"
  />
</template>
