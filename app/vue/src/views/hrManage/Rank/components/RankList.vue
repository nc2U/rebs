<script lang="ts" setup="">
import { ref } from 'vue'
import { headerSecondary } from '@/utils/cssMixins'
import Rank from './Rank.vue'

const msg = ref('부서리스트')
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="5%" />
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
      <col width="35%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell scope="col">No</CTableHeaderCell>
        <CTableHeaderCell scope="col">구분</CTableHeaderCell>
        <CTableHeaderCell scope="col">직책</CTableHeaderCell>
        <CTableHeaderCell scope="col">직함</CTableHeaderCell>
        <CTableHeaderCell scope="col">설명</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Rank
        v-for="site in siteList"
        :key="site.pk"
        :site="site"
        :is-returned="isReturned"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    v-if="siteCount > 10"
    :active-page="1"
    :limit="8"
    :pages="sitePages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
