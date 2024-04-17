<script lang="ts" setup>
import { reactive, computed, inject, onBeforeMount, type ComputedRef, nextTick } from 'vue'
import type { ActLogEntryFilter, IssueProject } from '@/store/types/work'
import { useRoute } from 'vue-router'
import { useAccount } from '@/store/pinia/account'
import { dateFormat } from '@/utils/baseMixins'
import Cookies from 'js-cookie'
import DatePicker from '@/components/DatePicker/index.vue'

defineProps({
  hasSubs: { type: Boolean, default: false },
})

const emit = defineEmits(['filter-submit'])

const form = reactive<ActLogEntryFilter & { subProjects: boolean }>({
  project: '',
  project__search: '',
  to_act_date: dateFormat(new Date()),
  from_act_date: '',
  user: '',
  sort: ['1', '2', '9'],
  subProjects: true,
})

const syncComment = () => {
  nextTick(() => {
    if (form.sort?.includes('1')) form.sort.push('2')
    else form.sort = form.sort?.filter(item => item !== '2')
  })
}

const iProject = inject<ComputedRef<IssueProject>>('iProject')

const accStore = useAccount()
const userInfo = computed(() => accStore.userInfo)
const getUsers = computed(() =>
  iProject?.value
    ? iProject.value?.all_members.map(m => ({
        value: m.user.pk,
        label: m.user.username,
      }))
    : accStore.getUsers,
)

const route = useRoute()
const filterSubmit = () => {
  if (route.params.projId) {
    if (form.subProjects) {
      form.project = route.params.projId as string
      form.project__search = ''
    } else {
      form.project = ''
      form.project__search = route.params.projId as string
    }
  } else {
    form.project = ''
    form.project__search = ''
  }
  const toDate = new Date(form.to_act_date as string)
  form.to_act_date = dateFormat(toDate)
  form.from_act_date = dateFormat(new Date(toDate.getTime() - 9 * 24 * 60 * 60 * 1000))
  const cookieSort = form.sort ? form.sort?.sort().join('-') : ''
  Cookies.set('cookieSort', cookieSort)
  emit('filter-submit', { ...form })
}

onBeforeMount(() => {
  accStore.fetchUsersList()
  const cookieSort = Cookies.get('cookieSort')?.split('-') as (
    | '1'
    | '2'
    | '3'
    | '4'
    | '5'
    | '6'
    | '7'
    | '8'
    | '9'
  )[]
  if (cookieSort?.length) form.sort = cookieSort
})
</script>

<template>
  <CRow class="mb-3">
    <CCol><h6 class="asideTitle">작업내역</h6></CCol>
  </CRow>
  <CRow class="mb-2">
    <CFormLabel for="log-date" class="col-sm-4 col-form-label">10일 기록</CFormLabel>
    <CCol class="col-xxl-5">
      <DatePicker v-model="form.to_act_date" id="log-date" />
    </CCol>
  </CRow>

  <CRow class="mb-3">
    <CFormLabel for="log-user" class="col-sm-4 col-form-label">사용자</CFormLabel>
    <CCol class="col-xxl-5">
      <CFormSelect v-model="form.user" id="log-user" size="sm">
        <option>---------</option>
        <option :value="userInfo?.pk">&lt;&lt; 나 &gt;&gt;</option>
        <option v-for="user in getUsers" :value="user.value" :key="user.value">
          {{ user.label }}
        </option>
      </CFormSelect>
    </CCol>
  </CRow>

  <CRow class="mb-3">
    <CCol>
      <CFormCheck
        v-model="form.sort"
        value="1"
        label="업무"
        id="issue-filter"
        @change="syncComment"
      />
      <CFormCheck v-model="form.sort" value="3" label="변경묶음" id="changeset-filter" />
      <CFormCheck v-model="form.sort" value="4" label="공지" id="news-filter" />
      <CFormCheck v-model="form.sort" value="5" label="문서" id="docs-filter" />
      <CFormCheck v-model="form.sort" value="6" label="파일" id="file-filter" />
      <CFormCheck v-model="form.sort" value="7" label="위키 편집" id="wiki-filter" />
      <CFormCheck v-model="form.sort" value="8" label="글" id="message-filter" />
      <CFormCheck v-model="form.sort" value="9" label="작업시간" id="spent-time-filter" />
    </CCol>
  </CRow>

  <CRow v-if="hasSubs" class="mb-3">
    <CCol>
      <CFormCheck v-model="form.subProjects" label="하위 프로젝트" id="sub-project-filter" />
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CButton color="dark" size="sm" @click="filterSubmit">적용</CButton>
    </CCol>
  </CRow>
</template>

<style lang="scss" scoped>
.asideTitle {
  font-size: 1.1em;
}
</style>
