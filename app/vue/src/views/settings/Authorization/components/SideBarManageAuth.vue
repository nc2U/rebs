<script lang="ts" setup>
import { ref, reactive, computed, watch, nextTick } from 'vue'
import { MenuType } from '../index.vue'

const props = defineProps({
  user: { type: Object, default: null },
})

const emit = defineEmits(['select-auth'])

const auth = ref<MenuType>({
  contract: '0',
  payment: '0',
  notice: '0',
  project_cash: '0',
  project_docs: '0',
  project: '0',
  company_cash: '0',
  company_docs: '0',
  human_resource: '0',
  company_settings: '0',
  auth_manage: '0',
})
const auths = reactive([
  { label: '권한없음', value: '0' },
  { label: '읽기권한', value: '1' },
  { label: '쓰기권한', value: '2' },
])
const isInActive = computed(() => !props.user)

const getColor = (status: '0' | '1' | '2') => {
  if (status === '1') return 'yellow-darken-2'
  else if (status === '2') return 'success'
  else return 'blue-grey-lighten-1'
}

const selectAuth = () => nextTick(() => emit('select-auth', auth.value))

watch(
  () => props.user,
  newValue => {
    if (newValue && newValue?.staffauth) {
      auth.value.contract = newValue.staffauth.contract
      auth.value.payment = newValue.staffauth.payment
      auth.value.notice = newValue.staffauth.notice
      auth.value.project_cash = newValue.staffauth.project_cash
      auth.value.project_docs = newValue.staffauth.project_docs
      auth.value.project = newValue.staffauth.project
      auth.value.company_cash = newValue.staffauth.company_cash
      auth.value.company_docs = newValue.staffauth.company_docs
      auth.value.human_resource = newValue.staffauth.human_resource
      auth.value.company_settings = newValue.staffauth.company_settings
      auth.value.auth_manage = newValue.staffauth.auth_manage
    } else {
      auth.value.contract = '0'
      auth.value.payment = '0'
      auth.value.notice = '0'
      auth.value.project_cash = '0'
      auth.value.project_docs = '0'
      auth.value.project = '0'
      auth.value.company_cash = '0'
      auth.value.company_docs = '0'
      auth.value.human_resource = '0'
      auth.value.company_settings = '0'
      auth.value.auth_manage = '0'
    }
  },
)
</script>

<template>
  <Crow>
    <CCol>
      <CRow class="mb-3">
        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.contract)"
                />
                분양계약 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.contract"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.payment)"
                />
                분양수납 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.payment"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.notice)"
                />
                고객고지 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.notice"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.project_cash)"
                />
                현장자금 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.project_cash"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.project_docs)"
                />
                현장문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.project_docs"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.project)"
                />
                신규 프로젝트
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.project"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.company_cash)"
                />
                본사회계 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.company_cash"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.company_docs)"
                />
                본사문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.company_docs"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.human_resource)"
                />
                본사인사 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.human_resource"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.company_settings)"
                />
                회사관련 설정
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.company_settings"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.auth_manage)"
                />
                권한설정 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.auth_manage"
                  :options="auths"
                  :disabled="isInActive"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1"></CRow>
          </CCol>
        </CRow>
      </CRow>
    </CCol>
  </Crow>
</template>
