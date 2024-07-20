<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin2'
import { useCompany } from '@/store/pinia/company'
import { write_human_resource } from '@/utils/pageAuth'
import { type Position, type ComFilter } from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddPosition from './components/AddPosition.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import PositionList from './components/PositionList.vue'

// 직위 = Position
const refListControl = ref()

const dataFilter = ref<ComFilter>({
  page: 1,
  com: 1,
  q: '',
})

const comStore = useCompany()
const company = computed(() => comStore.company?.pk)
const comName = computed(() => comStore.company?.name || undefined)

const excelUrl = computed(
  () => `/excel/positions/?company=${company.value}&search=${dataFilter.value.q}`,
)

const listFiltering = (payload: ComFilter) => {
  dataFilter.value = payload
  if (company.value)
    fetchPositionList({
      page: payload.page,
      com: payload.com,
      q: payload.q,
    })
}

const fetchAllGradeList = (com?: number) => comStore.fetchAllGradeList(com)
const fetchPositionList = (payload: ComFilter) => comStore.fetchPositionList(payload)

const createPosition = (payload: Position, p?: number, c?: number) =>
  comStore.createPosition(payload, p, c)
const updatePosition = (payload: Position, p?: number, c?: number) =>
  comStore.updatePosition(payload, p, c)
const deletePosition = (pk: number, com: number) => comStore.deletePosition(pk, com)

const multiSubmit = (payload: Position) => {
  const { page } = dataFilter.value
  if (company.value) {
    if (!!payload.pk) updatePosition(payload, page, company.value)
    else createPosition(payload, page, company.value)
  }
}
const onDelete = (pk: number) => {
  if (company.value) deletePosition(pk, company.value)
}

const pageSelect = (num: number) => {
  dataFilter.value.page = num
  if (company.value) {
    dataFilter.value.com = company.value
    fetchPositionList(dataFilter.value)
  }
}

const dataSetup = (pk: number) => {
  fetchAllGradeList(pk)
  fetchPositionList({ com: pk })
}

const dataReset = () => {
  comStore.allGradeList = []
  comStore.positionList = []
}

const comSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

onMounted(() => dataSetup(company.value || comStore.initComId))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="CompanySelect"
    @com-select="comSelect"
  />
  <ContentBody>
    <CCardBody>
      <ListController ref="refListControl" @list-filtering="listFiltering" />
      <AddPosition v-if="write_human_resource" :company="comName" @multi-submit="multiSubmit" />
      <TableTitleRow title="직위 목록" excel :url="excelUrl" :disabled="!company" />
      <PositionList @multi-submit="multiSubmit" @on-delete="onDelete" @page-select="pageSelect" />
    </CCardBody>
  </ContentBody>
</template>
