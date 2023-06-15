<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin2'
import { useCompany } from '@/store/pinia/company'
import { Position, ComFilter } from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddPosition from './components/AddPosition.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import PositionList from './components/PositionList.vue'

const listControl = ref()

const dataFilter = ref<ComFilter>({
  page: 1,
  com: 1,
  q: '',
})

const companyStore = useCompany()
const initComId = computed(() => companyStore.initComId)
const comId = computed(() => companyStore.company?.pk)
const comName = computed(() => companyStore.company?.name || undefined)

const companySelect = (target: number) => {
  if (!!target) {
    fetchAllGradeList(target)
    fetchPositionList({ com: target })
  } else {
    companyStore.allGradeList = []
    companyStore.positionList = []
  }
}

const listFiltering = (payload: ComFilter) => {
  dataFilter.value = payload
  if (comId.value)
    fetchPositionList({
      page: payload.page,
      com: payload.com,
      q: payload.q,
    })
}

const fetchAllGradeList = (com?: number) => companyStore.fetchAllGradeList(com)
const fetchPositionList = (payload: ComFilter) =>
  companyStore.fetchPositionList(payload)

const createPosition = (payload: Position, p?: number, c?: number) =>
  companyStore.createPosition(payload, p, c)
const updatePosition = (payload: Position, p?: number, c?: number) =>
  companyStore.updatePosition(payload, p, c)
const deletePosition = (pk: number, com: number) =>
  companyStore.deletePosition(pk, com)

const multiSubmit = (payload: Position) => {
  const { page } = dataFilter.value
  if (comId.value) {
    if (!!payload.pk) updatePosition(payload, page, comId.value)
    else createPosition(payload, page, comId.value)
  }
}
const onDelete = (pk: number) => {
  if (comId.value) deletePosition(pk, comId.value)
}

const pageSelect = (num: number) => {
  dataFilter.value.page = num
  if (comId.value) {
    dataFilter.value.com = comId.value
    fetchPositionList(dataFilter.value)
  }
}

onMounted(() => {
  const companyPk = comId.value || initComId.value
  fetchAllGradeList(companyPk)
  fetchPositionList({ com: companyPk })
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="companySelect"
  />
  <ContentBody>
    <CCardBody>
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddPosition :company="comName" @multi-submit="multiSubmit" />
      <TableTitleRow title="직위 목록" excel url="#" disabled />
      <PositionList
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @page-select="pageSelect"
      />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
