<script lang="ts" setup>
import { reactive, computed, inject, onBeforeMount, type ComputedRef } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { dateFormat } from '@/utils/baseMixins'
import type { IssueProject } from '@/store/types/work'
import DatePicker from '@/components/DatePicker/index.vue'

defineProps({
  hasSubs: { type: Boolean, default: false },
})

const emit = defineEmits(['filter-submit'])

const form = reactive({
  to_act_date: dateFormat(new Date()),
  from_act_date: '',
  user: null as number | null,
  issue: true,
  changeSet: false,
  news: false,
  docs: false,
  file: false,
  wiki: false,
  message: false,
  spentTime: true,
  subProjects: true,
})

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

const filterSubmit = () => {
  const toDate = new Date(form.to_act_date)
  form.to_act_date = dateFormat(toDate)
  form.from_act_date = dateFormat(new Date(toDate.getTime() - 9 * 24 * 60 * 60 * 1000))
  emit('filter-submit', { ...form })
}

onBeforeMount(() => {
  accStore.fetchUsersList()
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
      <CFormCheck v-model="form.issue" label="업무" id="issue-filter" />
      <CFormCheck v-model="form.changeSet" label="변경묶음" id="changeset-filter" disabled />
      <CFormCheck v-model="form.news" label="공지" id="news-filter" disabled />
      <CFormCheck v-model="form.docs" label="문서" id="docs-filter" disabled />
      <CFormCheck v-model="form.file" label="파일" id="file-filter" disabled />
      <CFormCheck v-model="form.wiki" label="위키 편집" id="wiki-filter" disabled />
      <CFormCheck v-model="form.message" label="글" id="message-filter" disabled />
      <CFormCheck v-model="form.spentTime" label="작업시간" id="spent-time-filter" />
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
