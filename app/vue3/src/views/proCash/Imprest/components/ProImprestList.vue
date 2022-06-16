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
        <CTableHeaderCell scope="col">계정</CTableHeaderCell>
        <CTableHeaderCell scope="col">
          세부계정
          <router-link to="" @click="showD1">
            <CIcon name="cilCog" @click="$refs.DAccount.callModal()" />
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

  <AlertModal ref="DAccount" size="lg">
    <template v-slot:header> 프로젝트 계정 분류 보기</template>
    <template v-slot:default>
      <CAccordion>
        <CAccordionItem
          v-for="d1 in allAccD1List"
          :key="d1.pk"
          :item-key="d1.pk"
        >
          <CAccordionHeader>
            {{ `[${d1.code}] ${d1.name} (${d1.description})` }}
          </CAccordionHeader>
          <CAccordionBody class="pl-3">
            <CRow
              v-for="d2 in allAccD2List.filter(d2 => d2.d1 === d1.pk)"
              :key="d2.pk"
              class="pl-2 mb-2"
            >
              <CCol>
                [{{ d2.code }}] {{ d2.name }} ------ ({{ d2.description }})
              </CCol>
            </CRow>
          </CAccordionBody>
        </CAccordionItem>
      </CAccordion>
    </template>
    <template v-slot:footer></template>
  </AlertModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ProImprest from '@/views/proCash/Imprest/components/ProImprest.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProImprestList',
  components: { ProImprest, AlertModal },
  props: { project: Object },
  computed: {
    ...mapGetters('proCash', ['proImprestPages', 'getProImprestLogs']),
    ...mapState('proCash', ['allAccD1List', 'allAccD2List']),
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
