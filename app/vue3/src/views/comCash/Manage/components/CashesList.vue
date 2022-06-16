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
        <CTableHeaderCell scope="col">
          세부계정
          <router-link to="" @click="showD1">
            <CIcon name="cilCog" @click="$refs.DAccount.callModal()" />
          </router-link>
        </CTableHeaderCell>
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

  <AlertModal ref="DAccount" size="lg">
    <template v-slot:header> 계정 분류 보기</template>
    <template v-slot:default>
      <CAccordion>
        <CAccordionItem
          v-for="d1 in listAccD1List"
          :item-key="d1.pk"
          :key="d1.pk"
        >
          <CAccordionHeader>{{
            `[${d1.code}] ${d1.name} (${d1.description})`
          }}</CAccordionHeader>
          <CAccordionBody class="pl-3">
            <CAccordion>
              <CAccordionItem
                v-for="d2 in listAccD2List.filter(a => a.d1 === d1.pk)"
                :item-key="d2.pk"
                :key="d2.pk"
              >
                <CAccordionHeader
                  >[{{ d2.code }}] {{ d2.name }} ------ ({{
                    d2.description
                  }})</CAccordionHeader
                >
                <CAccordionBody class="pl-3">
                  <CRow
                    v-for="d3 in listAccD3List.filter(a => a.d2 === d2.pk)"
                    :key="d3.pk"
                    class="pl-3 mb-2"
                  >
                    <CCol>
                      [{{ d3.code }}] {{ d3.name }} ------ ({{
                        d3.description
                      }})
                    </CCol>
                  </CRow>
                </CAccordionBody>
              </CAccordionItem>
            </CAccordion>
          </CAccordionBody>
        </CAccordionItem>
      </CAccordion>
    </template>
    <template v-slot:footer></template>
  </AlertModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Cashes from '@/views/comCash/Manage/components/Cashes.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'CashesList',
  components: { Cashes, AlertModal },
  props: { company: Object },
  computed: {
    ...mapGetters('comCash', ['cashesPages', 'getCashLogs']),
    ...mapState('comCash', ['listAccD1List', 'listAccD2List', 'listAccD3List']),
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
