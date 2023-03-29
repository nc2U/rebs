<script lang="ts" setup>
import { computed } from 'vue'
import { useProCash } from '@/store/pinia/proCash'
import { ProjectCashBook } from '@/store/types/proCash'
import { cutString } from '@/utils/baseMixins'
import { TableSecondary } from '@/utils/cssMixins'
import ProImprest from '@/views/proCash/Imprest/components/ProImprest.vue'
import Pagination from '@/components/Pagination'
import AlertModal from '@/components/Modals/AlertModal.vue'

const emit = defineEmits(['page-select', 'multi-submit', 'on-delete'])

const proCashStore = useProCash()
const allAccD1List = computed(() => proCashStore.allAccD1List)
const allAccD2List = computed(() => proCashStore.allAccD2List)

const proImprestList = computed(() => proCashStore.proImprestList)
const proImprestPages = computed(() => proCashStore.proImprestPages)

const pageSelect = (page: number) => emit('page-select', page)

const multiSubmit = (payload: {
  formData: ProjectCashBook
  sepData: ProjectCashBook | null
}) => emit('multi-submit', payload)

const onDelete = (payload: { project: number; pk: number }) =>
  emit('on-delete', payload)
</script>

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
      <CTableRow :color="TableSecondary" class="text-center">
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
        v-for="imprest in proImprestList"
        :key="imprest.pk"
        :imprest="imprest"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="proImprestPages(15)"
    class="mt-3"
    @active-page-change="pageSelect"
  />

  <AlertModal ref="DAccount" size="lg">
    <template #header> 프로젝트 계정 분류 보기</template>
    <template #default>
      <CAccordion>
        <CAccordionItem
          v-for="d1 in allAccD1List"
          :key="d1.pk"
          :item-key="d1.pk"
        >
          <CAccordionHeader>
            {{ `[${d1.code}] ${d1.name} :: ${cutString(d1.description, 45)}` }}
          </CAccordionHeader>
          <CAccordionBody class="pl-3">
            <CRow
              v-for="d2 in allAccD2List.filter(d2 => d2.d1 === d1.pk)"
              :key="d2.pk"
              class="pl-2 mb-2"
            >
              <CCol>
                [{{ d2.code }}] {{ d2.name }} ::
                {{ cutString(d2.description, 38) }}
              </CCol>
            </CRow>
          </CAccordionBody>
        </CAccordionItem>
      </CAccordion>
    </template>
    <template #footer></template>
  </AlertModal>
</template>
