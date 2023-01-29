<script lang="ts" setup="">
import { ref } from 'vue'
import { headerSecondary } from '@/utils/cssMixins'
import Staff from './Staff.vue'

const msg = ref('부서리스트')
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="10%" />
      <col width="20%" />
      <col width="20%" />
      <col width="50%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell rowspan="2" scope="col">No</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">상위부서</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">부서명</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">주요업무</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Staff
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
