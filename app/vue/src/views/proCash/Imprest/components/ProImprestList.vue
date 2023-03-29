<script lang="ts" setup>
import { computed } from 'vue'
import { useProCash } from '@/store/pinia/proCash'
import { ProjectCashBook } from '@/store/types/proCash'
import { TableSecondary } from '@/utils/cssMixins'
import ProImprest from '@/views/proCash/Imprest/components/ProImprest.vue'
import Pagination from '@/components/Pagination'
import AccDepth from '../../Manage/components/AccDepth.vue'

const emit = defineEmits(['page-select', 'multi-submit', 'on-delete'])

const proCashStore = useProCash()
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
          <a href="javascript:void(0)">
            <CIcon name="cilCog" @click="$refs.accDepth.callModal()" />
          </a>
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

  <AccDepth ref="accDepth" />
</template>
