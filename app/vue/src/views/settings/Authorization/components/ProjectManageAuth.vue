<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch, nextTick } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import Multiselect from '@vueform/multiselect'

const props = defineProps({
  user: { type: Object, default: undefined },
})

const emit = defineEmits(['get-allowed', 'get-assigned'])

const allowedProjects = ref<number[]>([])
const assignedProject = ref<number | null>(null)

const isInActive = computed(() => props.user === undefined)

const store = useStore()
const isDark = computed(() => store.state.theme === 'dark')

const project = useProject()
const getProjects = computed(() => project.getProjects)

const getAllowed = () => nextTick(() => emit('get-allowed', allowedProjects))
const getAssigned = () => nextTick(() => emit('get-assigned', assignedProject))

watch(
  () => props.user,
  newValue => {
    if (newValue?.staffauth) {
      allowedProjects.value = newValue.staffauth.allowed_projects
      assignedProject.value = newValue.staffauth.assigned_project
    }
  },
)

onBeforeMount(() => {
  project.fetchProjectList()
})
</script>

<template>
  <CCallout color="secondary" class="mb-4" :class="{ 'bg-light': !isDark }">
    <CRow>
      <CCol md="10" lg="8" xl="6">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label">
            허용 프로젝트
          </CFormLabel>
          <CCol>
            <Multiselect
              v-model="allowedProjects"
              :options="getProjects"
              placeholder="프로젝트"
              mode="tags"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
              :disabled="isInActive"
              @change="getAllowed"
            />
            <small class="form-text">
              사용자가 조회 및 관리할 수 있는 프로젝트들을 선택합니다.
            </small>
          </CCol>
        </CRow>
      </CCol>

      <CCol md="10" lg="8" xl="6">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label">
            담당 메인 프로젝트
          </CFormLabel>
          <CCol>
            <Multiselect
              v-model="assignedProject"
              :options="getProjects"
              placeholder="프로젝트"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
              :disabled="isInActive"
              @change="getAssigned"
            />
            <small class="form-text">
              사용자의 각 화면에서 선택한 프로젝트를 기본 프로젝트로 보여줍니다.
            </small>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
  <hr />
</template>
