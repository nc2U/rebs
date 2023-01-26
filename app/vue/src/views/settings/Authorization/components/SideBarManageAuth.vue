<script lang="ts" setup>
import { ref, reactive, computed, watch, nextTick } from 'vue'
import { UserAuth } from '../index.vue'

const props = defineProps({
  user: { type: Object, default: null },
})

const emit = defineEmits(['select-auth'])

const authData = ref<UserAuth>({
  pk: undefined,
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

const selectAuth = () =>
  nextTick(() => {
    const auth = { ...authData.value }
    auth.pk = props.user.staffauth.pk
    emit('select-auth', auth)
  })

watch(
  () => props.user,
  newValue => {
    if (newValue && newValue?.staffauth) {
      authData.value.pk = newValue.staffauth.pk
      authData.value.contract = newValue.staffauth.contract
      authData.value.payment = newValue.staffauth.payment
      authData.value.notice = newValue.staffauth.notice
      authData.value.project_cash = newValue.staffauth.project_cash
      authData.value.project_docs = newValue.staffauth.project_docs
      authData.value.project = newValue.staffauth.project
      authData.value.company_cash = newValue.staffauth.company_cash
      authData.value.company_docs = newValue.staffauth.company_docs
      authData.value.human_resource = newValue.staffauth.human_resource
      authData.value.company_settings = newValue.staffauth.company_settings
      authData.value.auth_manage = newValue.staffauth.auth_manage
    } else {
      authData.value.pk = undefined
      authData.value.contract = '0'
      authData.value.payment = '0'
      authData.value.notice = '0'
      authData.value.project_cash = '0'
      authData.value.project_docs = '0'
      authData.value.project = '0'
      authData.value.company_cash = '0'
      authData.value.company_docs = '0'
      authData.value.human_resource = '0'
      authData.value.company_settings = '0'
      authData.value.auth_manage = '0'
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
                  :color="getColor(authData.contract)"
                />
                분양계약 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.contract"
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
                  :color="getColor(authData.payment)"
                />
                분양수납 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.payment"
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
                  :color="getColor(authData.notice)"
                />
                고객고지 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.notice"
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
                  :color="getColor(authData.project_cash)"
                />
                현장자금 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.project_cash"
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
                  :color="getColor(authData.project_docs)"
                />
                현장문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.project_docs"
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
                  :color="getColor(authData.project)"
                />
                신규 프로젝트
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.project"
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
                  :color="getColor(authData.company_cash)"
                />
                본사회계 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.company_cash"
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
                  :color="getColor(authData.company_docs)"
                />
                본사문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.company_docs"
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
                  :color="getColor(authData.human_resource)"
                />
                본사인사 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.human_resource"
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
                  :color="getColor(authData.company_settings)"
                />
                회사관련 설정
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.company_settings"
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
                  :color="getColor(authData.auth_manage)"
                />
                권한설정 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.auth_manage"
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
