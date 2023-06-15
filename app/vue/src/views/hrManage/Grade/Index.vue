<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin2'
import { useCompany } from '@/store/pinia/company'
import { Grade, ComFilter } from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddGrade from './components/AddGrade.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import GradeList from './components/GradeList.vue'

const listControl = ref()

const dataFilter = ref<ComFilter>({
  page: 1,
  com: 1,
  q: '',
})

const comStore = useCompany()
const initComId = computed(() => comStore.initComId)
const comId = computed(() => comStore.company?.pk)
const comName = computed(() => comStore.company?.name || undefined)

const companySelect = (target: number) => {
  if (!!target) {
    fetchGradeList({ com: target })
    fetchAllPositionList(target)
  } else {
    comStore.gradeList = []
    comStore.allPositionList = []
  }
}

const listFiltering = (payload: ComFilter) => {
  dataFilter.value = payload
  if (comId.value)
    fetchGradeList({
      page: payload.page,
      com: payload.com,
      q: payload.q,
    })
}

const fetchGradeList = (payload: ComFilter) => comStore.fetchGradeList(payload)
const fetchAllPositionList = (com?: number) =>
  comStore.fetchAllPositionList(com)

const createGrade = (payload: Grade, p?: number, c?: number) =>
  comStore.createGrade(payload, p, c)
const updateGrade = (payload: Grade, p?: number, c?: number) =>
  comStore.updateGrade(payload, p, c)
const deleteGrade = (pk: number, com: number) => comStore.deleteGrade(pk, com)

const multiSubmit = (payload: Grade) => {
  const { page } = dataFilter.value
  if (comId.value) {
    if (!!payload.pk) updateGrade(payload, page, comId.value)
    else createGrade(payload, page, comId.value)
  }
}
const onDelete = (pk: number) => {
  if (comId.value) deleteGrade(pk, comId.value)
}

const pageSelect = (num: number) => {
  dataFilter.value.page = num
  if (comId.value) {
    dataFilter.value.com = comId.value
    fetchGradeList(dataFilter.value)
  }
}

onMounted(() => {
  const companyPk = comId.value || initComId.value
  fetchGradeList({ com: companyPk })
  fetchAllPositionList(companyPk)
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
      <AddGrade :company="comName" @multi-submit="multiSubmit" />
      <TableTitleRow title="직급 목록" excel url="#" disabled />
      <GradeList
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @page-select="pageSelect"
      />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
