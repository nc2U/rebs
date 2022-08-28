<script lang="ts" setup>
import { computed } from 'vue'
import { useSite } from '@/store/pinia/project_site'
import { headerSecondary } from '@/utils/cssMixins'
import Site from './Site.vue'
import Pagination from '@/components/Pagination'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({ isReturned: { type: Boolean } })
const emit = defineEmits(['page-select', 'on-delete', 'multi-submit'])

const siteStore = useSite()
const siteList = computed(() => siteStore.getSiteList)
const siteCount = computed(() => siteStore.siteCount)

const sitePages = (num: number) => Math.ceil(siteCount.value / num)
const pageSelect = (page: number) => emit('page-select', page)
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="6%" />
      <col width="7%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col width="8%" />
      <col v-if="isReturned" width="8%" />
      <col v-if="isReturned" width="8%" />
      <col width="33%" />
      <col width="6%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center">
        <CTableHeaderCell rowspan="2" scope="col">No</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">행정동</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">지번</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">지목</CTableHeaderCell>
        <CTableHeaderCell colspan="2" scope="col">공부상 면적</CTableHeaderCell>
        <CTableHeaderCell v-if="isReturned" colspan="2" scope="col">
          환지 면적
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">소유자 목록</CTableHeaderCell>
        <CTableHeaderCell rowspan="2" scope="col">비고</CTableHeaderCell>
      </CTableRow>
      <CTableRow class="text-center">
        <CTableHeaderCell scope="col">m<sup>2</sup></CTableHeaderCell>
        <CTableHeaderCell scope="col">평</CTableHeaderCell>
        <CTableHeaderCell v-if="isReturned" scope="col">
          m<sup>2</sup>
        </CTableHeaderCell>
        <CTableHeaderCell v-if="isReturned" scope="col">평</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Site
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
    :active-page="1"
    :limit="8"
    :pages="sitePages(10)"
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
          <CAccordionHeader
            >{{ `[${d1.code}] ${d1.name} (${d1.description})` }}
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
    <template #footer></template>
  </AlertModal>
</template>
