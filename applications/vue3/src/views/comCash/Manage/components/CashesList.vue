<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="8%" />
      <col width="5%" />
      <col width="5%" />
      <col width="9%" />
      <col width="15%" />
      <col width="11%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="11%" />
      <col width="6%" />
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
        <CTableHeaderCell scope="col">지출증빙</CTableHeaderCell>
        <CTableHeaderCell scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Cashes
        v-for="cash in getCashLogs"
        :cash="cash"
        :key="cash.pk"
        @on-update="onUpdate"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <CSmartPagination
    :activePage="1"
    :limit="8"
    :pages="cashesPages(15)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Cashes from '@/views/comCash/Manage/components/Cashes.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'CashesList',
  components: { Cashes },
  props: { company: Object },
  computed: {
    ...mapGetters('comCash', ['cashesPages', 'getCashLogs']),
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
