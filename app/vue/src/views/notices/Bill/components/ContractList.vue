<script lang="ts" setup>
import { computed, ref, nextTick } from 'vue'
import { useStore } from 'vuex'
import Contract from '@/views/notices/Bill/components/Contract.vue'
import Pagination from '@/components/Pagination'
import { headerSecondary } from '@/utils/cssMixins'

defineProps({ nowOrder: { type: Number, default: null } })
const emit = defineEmits(['page-select', 'on-ctor-chk', 'all-un-checked'])

const page = ref(1)
const allChecked = ref(false)

const store = useStore()

const contBillIndex = computed(() => store.getters['contract/contBillIndex'])
const contractPages = computed(() => store.getters['contract/contractPages'])

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

const unChk = () => {
  page.value = 2
  setTimeout(() => {
    page.value = 1
  }, 50)
}
defineExpose({ unChk })
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

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center">
        <CTableHeaderCell scope="col">
          <CFormCheck
            id="checkAll"
            v-model="allChecked"
            label="전체"
            @change="allUnChecked"
          />
        </CTableHeaderCell>
        <CTableHeaderCell scope="col">계약 일련번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">차수</CTableHeaderCell>
        <CTableHeaderCell scope="col">타입</CTableHeaderCell>
        <CTableHeaderCell scope="col">동호수</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약자</CTableHeaderCell>
        <CTableHeaderCell scope="col">납입금액합계</CTableHeaderCell>
        <CTableHeaderCell scope="col">납입상태 (완납회차)</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약일자</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Contract
        v-for="contract in contBillIndex"
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
