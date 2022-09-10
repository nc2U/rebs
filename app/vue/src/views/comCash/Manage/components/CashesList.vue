<script lang="ts" setup>
import { computed } from 'vue'
import { useComCash } from '@/store/pinia/comCash'
import { CashBook } from '@/store/types/comCash'
import Cashes from '@/views/comCash/Manage/components/Cashes.vue'
import Pagination from '@/components/Pagination'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { headerSecondary } from '@/utils/cssMixins'

defineProps({ company: { type: Object, default: null } })

const emit = defineEmits(['page-select', 'on-update', 'on-delete'])

const useComCashStore = useComCash()
const cashesPages = computed(() => useComCashStore.cashesPages)
const getCashLogs = computed(() => useComCashStore.getCashLogs)
const listAccD1List = computed(() => useComCashStore.listAccD1List)
const listAccD2List = computed(() => useComCashStore.listAccD2List)
const listAccD3List = computed(() => useComCashStore.listAccD3List)

const pageSelect = (page: number) => emit('page-select', page)
const onUpdate = (payload: CashBook) => emit('on-update', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

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
      <CTableRow :color="headerSecondary" class="text-center">
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
        :key="cash.pk"
        :cash="cash"
        @on-update="onUpdate"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="cashesPages(15)"
    class="mt-3"
    @active-page-change="pageSelect"
  />

  <AlertModal ref="DAccount" size="lg">
    <template #header> 계정 분류 보기</template>
    <template #default>
      <CAccordion>
        <CAccordionItem
          v-for="d1 in listAccD1List"
          :key="d1.pk"
          :item-key="d1.pk"
        >
          <CAccordionHeader
            >{{ `[${d1.code}] ${d1.name} (${d1.description})` }}
          </CAccordionHeader>
          <CAccordionBody class="pl-3">
            <CAccordion>
              <CAccordionItem
                v-for="d2 in listAccD2List.filter(a => a.d1 === d1.pk)"
                :key="d2.pk"
                :item-key="d2.pk"
              >
                <CAccordionHeader
                  >[{{ d2.code }}] {{ d2.name }} ------ ({{ d2.description }})
                </CAccordionHeader>
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
    <template #footer></template>
  </AlertModal>
</template>
