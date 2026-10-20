<script lang="ts" setup>
import { computed, nextTick, onBeforeMount, ref, watch } from 'vue'
import { onBeforeRouteLeave, useRoute, useRouter } from 'vue-router'
import { navMenu, pageTitle } from '@/views/projects/_menu/headermixin2'
import { numFormat } from '@/utils/baseMixins'
import { usePerms } from '@/composables/usePerms'
import { useProject } from '@/store/pinia/project'
import { type ContFilter, useSite } from '@/store/pinia/project_site'
import type { Project, SiteContract } from '@/store/types/project'
import Loading from '@/components/Loading/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ProjectAuthGuard from '@/components/AuthGuard/ProjectAuthGuard.vue'
import ListController from './components/ListController.vue'
import AddSiteContract from './components/AddSiteContract.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import SiteContractList from './components/SiteContractList.vue'

const { can, PERM } = usePerms()
const canSiteRead = computed(() => can(PERM.SITE_READ))
const canSiteCreate = computed(() => can(PERM.SITE_CREATE))

const route = useRoute()
const router = useRouter()

// URL에서 highlight_id 파라미터 읽기
const highlightId = computed(() => {
  const id = route.query.highlight_id
  return id ? parseInt(id as string, 10) : null
})

// URL에서 project 파라미터 읽기
const urlProjectId = computed(() => {
  const id = route.query.project
  return id ? parseInt(id as string, 10) : null
})

const dataFilter = ref<ContFilter>({
  project: null,
  limit: '',
  page: 1,
  own_sort: '',
  search: '',
})

const projStore = useProject()
const project = computed(() => (projStore.project as Project)?.pk)

const siteStore = useSite()
const getContsTotal = computed(() => siteStore.getContsTotal?.contracted_area)

const excelUrl = computed(() => {
  const url = `/excel/sites-contracts/?project=${project.value}`
  const filter = dataFilter.value
  let queryStr = filter.own_sort ? `&own_sort=${filter.own_sort}` : ''
  queryStr = filter.search ? `${queryStr}&search=${filter.search}` : queryStr
  return `${url}${queryStr}`
})

const listFiltering = (payload: ContFilter) => {
  clearQueryString()
  if (project.value) {
    payload.project = project.value
    dataFilter.value = payload
    siteStore.fetchSiteContList(payload)
  }
}

// 하이라이트 기능
const scrollToHighlight = async () => {
  if (highlightId.value) {
    await nextTick()
    const element = document.querySelector(`[data-site-contract-id="${highlightId.value}"]`)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }
}

// 하이라이트 페이지 로드 함수
const loadHighlightPage = async (projectId: number) => {
  if (highlightId.value && projectId) {
    try {
      const pageParam = route.query.page
      let targetPage = pageParam ? parseInt(pageParam as string, 10) : 1
      if (!pageParam) {
        targetPage = await siteStore.findSiteContractPage(highlightId.value, {
          project: projectId,
        })
      }
      dataFilter.value = {
        project: projectId,
        limit: dataFilter.value.limit || '',
        page: targetPage,
        own_sort: dataFilter.value.own_sort || '',
        search: dataFilter.value.search || '',
      }
      siteStore.fetchSiteContList({ project: projectId, page: targetPage })
    } catch (error) {
      console.error('Error loading highlight page:', error)
      dataSetup(projectId)
    }
  }
}

const onCreate = (payload: FormData) => siteStore.createSiteCont(payload)

const onUpdate = (pk: number, payload: FormData) => siteStore.updateSiteCont(pk, payload)

const multiSubmit = (payload: SiteContract | FormData) => {
  if (payload instanceof FormData) {
    const pk = payload.get('pk')
    if (pk) onUpdate(Number(pk), payload)
    else onCreate(payload)
    return
  }

  const { pk, ...data } = payload as { [key: string]: any }
  const form = new FormData()

  for (const key in data) {
    if (key === 'site_cont_files') continue
    if (key === 'new_files' && Array.isArray(data[key])) {
      data[key].forEach((file: File) => form.append('new_files', file))
    } else if (key === 'del_files' && Array.isArray(data[key])) {
      data[key].forEach((id: number) => form.append('del_files', id.toString()))
    } else if (data[key] !== null && data[key] !== undefined && data[key] !== '') {
      form.set(key, data[key])
    }
  }

  if (pk) onUpdate(pk, form)
  else onCreate(form)
}

const onDelete = (payload: { pk: number; project: number }) => {
  const { pk, project: projId } = payload
  siteStore.deleteSiteCont(pk, projId)
}

const dataSetup = (pk: number) => {
  dataFilter.value.project = pk
  siteStore.fetchSiteContList(dataFilter.value)
  siteStore.fetchAllOwners(pk)
}

const dataReset = () => {
  siteStore.siteContList = []
  siteStore.siteContCount = 0
}

const projSelect = (target: number | null) => {
  clearQueryString()
  dataReset()
  if (target) dataSetup(target)
}

const pageSelect = (page: number) => {
  clearQueryString()
  dataFilter.value.page = page
  if (project.value) dataSetup(project.value)
}

// Query string 정리 함수
const clearQueryString = () => {
  if (route.query.page || route.query.highlight_id) {
    router
      .replace({
        name: route.name,
        params: route.params,
        query: {},
      })
      .catch(() => {
        // 동일 경로 이동 NavigationDuplicated 무시
      })
  }
}

watch(
  () => project.value,
  newVal => {
    clearQueryString()
    dataReset()
    if (newVal) dataSetup(newVal)
  },
)

onBeforeRouteLeave(() => {
  clearQueryString()
})

const loading = ref(true)
onBeforeMount(async () => {
  if (canSiteRead.value) {
    let projectId = urlProjectId.value || project.value || projStore.currentProject
    if (projectId) {
      if (urlProjectId.value && urlProjectId.value !== project.value) {
        console.log(`Using project ${urlProjectId.value} from URL parameter`)
        projectId = urlProjectId.value
      }

      siteStore.fetchAllOwners(projectId)

      if (highlightId.value) {
        await loadHighlightPage(projectId)
        await scrollToHighlight()
      } else {
        dataSetup(projectId)
      }
    }
  }
  loading.value = false
})
</script>

<template>
  <ProjectAuthGuard>
    <Loading v-model:active="loading" />
    <ContentHeader
      :page-title="pageTitle"
      :nav-menu="navMenu"
      selector="ProjectSelect"
      @proj-select="projSelect"
    />

    <ContentBody>
      <CCardBody class="pb-5">
        <ListController
          :project="project ?? undefined"
          @list-filtering="listFiltering"
        />
        <AddSiteContract
          v-if="canSiteCreate"
          :project="project ?? undefined"
          @multi-submit="multiSubmit"
        />
        <TableTitleRow
          title="부지 매입계약 목록"
          excel
          :url="excelUrl"
          filename="부지매입_계약목록.xlsx"
          :disabled="!project"
        >
          <span v-if="project" class="text-success" style="padding-top: 7px">
            총 계약 면적 :
            {{ numFormat(getContsTotal || 0, 2) }}
            m<sup>2</sup> ({{ numFormat((getContsTotal || 0) * 0.3025, 2) }}
            평) 등록
          </span>
        </TableTitleRow>
        <SiteContractList
          :limit="Number(dataFilter.limit) || 10"
          :highlight-id="highlightId ?? undefined"
          :current-page="dataFilter.page"
          @page-select="pageSelect"
          @multi-submit="multiSubmit"
          @on-delete="onDelete"
        />
      </CCardBody>
    </ContentBody>
  </ProjectAuthGuard>
</template>
