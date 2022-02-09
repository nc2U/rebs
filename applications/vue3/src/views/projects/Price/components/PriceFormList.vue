<template>
  <CTable hover responsive>
    <colgroup>
      <col width="15%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
      <col width="15%" />
    </colgroup>
    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell>차수</CTableHeaderCell>
        <CTableHeaderCell>타입</CTableHeaderCell>
        <CTableHeaderCell>층별 조건</CTableHeaderCell>
        <CTableHeaderCell>건물가(단위:원)</CTableHeaderCell>
        <CTableHeaderCell>대지가(단위:원)</CTableHeaderCell>
        <CTableHeaderCell>부가세(단위:원)</CTableHeaderCell>
        <CTableHeaderCell>분양가격(단위:원)</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="selected">
      <Price :price="priceList" :msg="msg" :cond-texts="condTexts" />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell colspan="7" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Price from '@/views/projects/Price/components/Price.vue'

export default defineComponent({
  name: 'PriceFormList',
  components: { Price },
  props: {
    project: {
      type: Object,
    },
    selected: {
      type: Boolean,
    },
    msg: {
      type: String,
    },
    condTexts: {
      type: Object,
    },
  },
})
</script>
