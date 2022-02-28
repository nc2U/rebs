<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="8%"/>
      <col width="6%"/>
      <col width="7%"/>
      <col width="10%"/>
      <col width="12%"/>
      <col width="10%"/>
      <col width="10%"/>
      <col width="10%"/>
      <col width="10%"/>
      <col width="9%"/>
      <col width="8%"/>
    </colgroup>

    <CTableHead>
      <CTableRow color="dark" class="text-center">
        <CTableHeaderCell scope="col">거래일자</CTableHeaderCell>
        <CTableHeaderCell scope="col">구분</CTableHeaderCell>
        <CTableHeaderCell scope="col">계정</CTableHeaderCell>
        <CTableHeaderCell scope="col">세부계정</CTableHeaderCell>
        <CTableHeaderCell scope="col">적요</CTableHeaderCell>
        <CTableHeaderCell scope="col">거래처</CTableHeaderCell>
        <CTableHeaderCell scope="col">거래계좌</CTableHeaderCell>
        <CTableHeaderCell scope="col">입금액</CTableHeaderCell>
        <CTableHeaderCell scope="col">출금액</CTableHeaderCell>
        <CTableHeaderCell scope="col">증빙자료</CTableHeaderCell>
        <CTableHeaderCell scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <ProCash
          v-for="proCash in getProCashLogs"
          :proCash="proCash"
          :key="proCash.pk"
          @on-update="onUpdate"
          @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <CSmartPagination
      :activePage="1"
      :limit="8"
      :pages="proCashPages(15)"
      class="mt-3"
      @active-page-change="pageSelect"
  />
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import ProCash from '@/views/proCash/Manage/components/ProCash.vue'
import {mapGetters} from 'vuex'

export default defineComponent({
  name: 'ProCashList',
  components: {ProCash},
  props: {project: Object},
  computed: {
    ...mapGetters('proCash', ['proCashPages', 'getProCashLogs']),
  },
  methods: {
    pageSelect(page: number) {
      this.$emit('page-select', page)
    },
    onUpdate(payload: any) {
      this.$emit('on-update', payload)
    },
    onDelete(pk: number) {
      this.$emit('on-delete', pk)
    },
  },
})
</script>
