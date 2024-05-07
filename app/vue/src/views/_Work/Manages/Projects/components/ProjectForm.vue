<script lang="ts" setup>
import Cookies from 'js-cookie'
import {
  ref,
  reactive,
  inject,
  onBeforeMount,
  onMounted,
  onUpdated,
  type PropType,
  nextTick,
} from 'vue'
import { useRoute } from 'vue-router'
import { colorLight } from '@/utils/cssMixins'
import type { IssueProject } from '@/store/types/work'
import MdEditor from '@/components/MdEditor/Index.vue'
import MultiSelect from '@/components/MultiSelect/index.vue'

const props = defineProps({
  title: { type: String, default: '' },
  project: { type: Object as PropType<IssueProject | null>, default: null },
  allProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
  allRoles: { type: Array as PropType<{ value: number; label: string }[]>, default: () => [] },
  allTrackers: { type: Array as PropType<{ value: number; label: string }[]>, default: () => [] },
})

const emit = defineEmits(['aside-visible', 'on-submit'])

const isDark = inject('isDark')

const validated = ref(false)

const form = reactive({
  pk: undefined as number | undefined,
  name: '',
  description: '',
  homepage: null as string | null,
  is_public: true,
  parent: null as number | null,
  slug: '',
  is_inherit_members: false,
  roles: [1, 2, 3],
  trackers: [1, 2, 3],
})

const tempSpace = ref('')

const chkPublic = () =>
  nextTick(() => {
    const parent = form.parent ? props.allProjects.filter(p => p.pk === form.parent)[0] : null
    form.is_public = !!parent?.is_public
    form.is_inherit_members = true
  })

const getSlug = (event: { key: string; code: string }) => {
  if (!props.project?.slug) {
    const pattern = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/ //한글

    let slug = form.slug.length === 0 ? '' : form.slug

    if (event.code === 'Backspace') {
      if (slug.length >= form.name.length) slug = slug.slice(0, -1)
    } else if (event.code === 'Space') tempSpace.value = !!slug.length ? '-' : ''
    else if (
      event.code.includes('Digit') ||
      (event.code.includes('Key') && event.key.length === 1 && !pattern.test(event.key))
    ) {
      if (event.key !== 'Process') {
        slug = slug + tempSpace.value + event.key.toLowerCase()
        tempSpace.value = ''
      }
    }

    form.slug = slug
  }
}

const module = reactive({
  issue: true,
  time: true,
  news: true,
  document: true,
  file: true,
  wiki: true,
  repository: false,
  forum: true,
  // calendar: true,
  // gantt: true,
})

const route = useRoute()

const onSubmit = (event: Event) => {
  const el = event.currentTarget as HTMLFormElement
  if (!el.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()
    validated.value = true
  } else {
    Cookies.set('workSettingMenu', '프로젝트')
    emit('on-submit', { ...form, ...module })
    validated.value = false
  }
}

const dataSetup = () => {
  if (props.project) {
    form.pk = props.project.pk
    form.name = props.project.name
    form.description = props.project.description
    form.slug = props.project.slug
    form.homepage = props.project.homepage
    form.is_public = props.project.is_public
    form.parent = props.project.parent
    form.is_inherit_members = props.project.is_inherit_members
    form.roles = props.project.roles?.map(r => r.pk)
    form.trackers = props.project.trackers?.map(t => t.pk)

    module.issue = !!props.project.module?.issue
    module.time = !!props.project.module?.time
    module.news = !!props.project.module?.news
    module.document = !!props.project.module?.document
    module.file = !!props.project.module?.file
    module.wiki = !!props.project.module?.wiki
    module.repository = !!props.project.module?.repository
    module.forum = !!props.project.module?.forum
    // module.calendar = !!props.project.module?.calendar
    // module.gantt = !!props.project.module?.gantt

    if (props.project.parent) chkPublic()
  }
}

onMounted(() => dataSetup())
onUpdated(() => dataSetup())
onBeforeMount(() => {
  emit('aside-visible', false)
  if (!!route.query.parent) {
    form.parent = Number(route.query.parent)
    chkPublic()
  }
})
</script>

<template>
  <CRow v-if="title" class="py-2">
    <CCol>
      <h5>{{ title }}</h5>
    </CCol>
  </CRow>

  <slot></slot>

  <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="onSubmit">
    <CCard :color="colorLight" class="mb-3">
      <CCardBody>
        <CRow class="mb-3">
          <CFormLabel class="required col-form-label text-right col-2">이름</CFormLabel>
          <CCol>
            <CFormInput
              v-model="form.name"
              @keydown="getSlug"
              maxlength="100"
              required
              placeholder="프로젝트 이름"
            />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">설명</CFormLabel>
          <CCol>
            <MdEditor v-model="form.description" placeholder="프로젝트 설명" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="required col-form-label text-right col-2">식별자</CFormLabel>
          <CCol>
            <CFormInput
              v-model="form.slug"
              maxlength="100"
              placeholder="프로젝트 식별자"
              required
              :disabled="!!project?.slug"
              text="1에서 100글자 소문자(a-z), 숫자, 대쉬(-)와 밑줄(_)만 가능합니다. 식별자 저장 후에는 수정할 수 없습니다."
            />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">홈페이지</CFormLabel>
          <CCol>
            <CFormInput v-model="form.homepage" maxlength="255" placeholder="홈페이지 URL" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">공개여부</CFormLabel>
          <CCol class="pt-2">
            <CFormSwitch
              v-model="form.is_public"
              id="is_public"
              label="프로젝트 공개 여부"
              :disabled="form.parent"
            />
            <div class="form-text">
              공개 프로젝트는 네트워크의 모든 사용자가 접속할 수 있습니다.
            </div>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">상위 프로젝트</CFormLabel>
          <CCol>
            <CFormSelect v-model.number="form.parent" @change="chkPublic">
              <option value="">상위 프로젝트 선택</option>
              <option
                v-for="proj in allProjects"
                :value="proj.pk"
                :key="proj.pk"
                v-show="project?.pk !== proj.pk"
              >
                <span v-if="proj.depth === 2"> &nbsp;&nbsp;» </span>
                <span v-if="proj.depth === 3"> &nbsp;&nbsp;&nbsp;&nbsp;» </span>
                <span v-if="proj.depth === 4"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;» </span>
                <span v-if="proj.depth === 5">
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;»
                </span>
                {{ proj.name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">상위 프로젝트 구성원 상속</CFormLabel>
          <CCol class="pt-2">
            <CFormSwitch
              v-model="form.is_inherit_members"
              id="is_inherit_members"
              label="상위 프로젝트 구성원 상속 여부"
              :disabled="!form.parent"
            />
          </CCol>
        </CRow>
        
        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">허용 역할</CFormLabel>
          <CCol class="pt-2">
            <MultiSelect v-model="form.roles" id="roles" :options="allRoles" />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-form-label text-right col-2">허용 유형</CFormLabel>
          <CCol class="pt-2">
            <MultiSelect v-model="form.trackers" id="trackers" :options="allTrackers" />
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>

    <h6>
      <v-icon icon="mdi-check-bold" size="sm" color="success" />
      모듈
    </h6>
    <CCard class="mb-3" :color="!isDark ? 'light' : ''">
      <CCardBody>
        <CRow>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.issue" id="issue" label="업무관리" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.time" id="time" label="시간추적" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.news" id="news" label="공지" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.document" id="document" label="문서" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.file" id="file" label="파일" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.wiki" id="wiki" label="위키" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.repository" id="repository" label="저장소" />
          </CCol>
          <CCol sm="6" md="4" lg="3" xl="2">
            <CFormCheck v-model="module.forum" id="forum" label="게시판" />
          </CCol>
          <!--          <CCol sm="6" md="4" lg="3" xl="2">-->
          <!--            <CFormCheck v-model="module.calendar" id="calendar" label="달력" />-->
          <!--          </CCol>-->
          <!--          <CCol sm="6" md="4" lg="3" xl="2">-->
          <!--            <CFormCheck v-model="module.gantt" id="gantt" label="Gantt 차트" />-->
          <!--          </CCol>-->
        </CRow>
      </CCardBody>
    </CCard>

    <CRow>
      <CCol>
        <CButton :color="!project ? 'primary' : 'success'" type="submit">저장</CButton>
        <!--        <CButton color="primary" type="submit">저장 후 계속하기</CButton>-->
      </CCol>
    </CRow>
  </CForm>
</template>
