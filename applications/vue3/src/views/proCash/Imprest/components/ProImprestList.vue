<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="8%" />
      <col width="6%" />
      <col width="7%" />
      <col width="10%" />
      <col width="12%" />
      <col width="11%" />
      <col width="11%" />
      <col width="10%" />
      <col width="10%" />
      <col width="9%" />
      <col width="6%" />
    </colgroup>

    <CTableHead>
      <CTableRow color="dark" class="text-center">
        <CTableHeaderCell scope="col">거래일자</CTableHeaderCell>
        <CTableHeaderCell scope="col">구분</CTableHeaderCell>
        <CTableHeaderCell scope="col">
          계정
          <router-link to="" @click="showD1">
            <CIcon name="cilDescription" />
          </router-link>
        </CTableHeaderCell>
        <CTableHeaderCell scope="col">
          세부계정
          <router-link to="" @click="showD1">
            <CIcon name="cilDescription" />
          </router-link>
        </CTableHeaderCell>
        <CTableHeaderCell scope="col">적요</CTableHeaderCell>
        <CTableHeaderCell scope="col">거래처</CTableHeaderCell>
        <CTableHeaderCell scope="col">
          거래계좌
          <!--          <router-link to="" @click="showD1">-->
          <CIcon name="cilCog" />
          <!--          </router-link>-->
        </CTableHeaderCell>
        <CTableHeaderCell scope="col">입금액</CTableHeaderCell>
        <CTableHeaderCell scope="col">출금액</CTableHeaderCell>
        <CTableHeaderCell scope="col">지출증빙</CTableHeaderCell>
        <CTableHeaderCell scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <ProImprest
        v-for="imprest in getProImprestLogs"
        :imprest="imprest"
        :key="imprest.pk"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <CSmartPagination
    :activePage="1"
    :limit="8"
    :pages="proImprestPages(15)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ProImprest from '@/views/proCash/Imprest/components/ProImprest.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ProImprestList',
  components: { ProImprest },
  props: { project: Object },
  computed: {
    ...mapGetters('proCash', ['proImprestPages', 'getProImprestLogs']),
  },
  methods: {
    pageSelect(page: number) {
      this.$emit('page-select', page)
    },
    onCreate(payload: any) {
      this.$emit('on-create', payload)
    },
    onUpdate(payload: any) {
      this.$emit('on-update', payload)
    },
    multiSubmit(payload: any) {
      this.$emit('multi-submit', payload)
    },
    onDelete(pk: number) {
      this.$emit('on-delete', pk)
    },
  },
})
</script>
