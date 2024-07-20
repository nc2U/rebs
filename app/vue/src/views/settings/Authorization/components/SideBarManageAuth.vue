<script lang="ts" setup>
import { ref, reactive, computed, nextTick, onMounted, onUpdated } from 'vue'
import { type UserAuth } from '@/views/settings/Authorization/Index.vue'
import { useStore } from '@/store'
import type { User } from '@/store/types/accounts'
import ProjectManageAuth from '@/views/settings/Authorization/components/ProjectManageAuth.vue'

const props = defineProps({
  user: { type: Object, default: null },
  allowed: { type: Array, default: () => [] },
})

const emit = defineEmits(['select-auth', 'get-allowed', 'get-assigned'])

const store = useStore()
const isDark = computed(() => store.theme === 'dark')

const authData = ref<UserAuth>({
  pk: undefined,
  contract: '0',
  payment: '0',
  notice: '0',
  project_cash: '0',
  project_docs: '0',
  project: '0',
  project_site: '0',
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

const isPrInActive = computed(() => !props.user || props.allowed?.length === 0)
const isCoInActive = computed(() => !props.user)

const getColor = (status: '0' | '1' | '2') => {
  if (status === '1') return ['yellow-darken-2', '#fcfced']
  else if (status === '2') return ['success', '#edf7f2']
  else return ['blue-grey-lighten-1', '']
}

const getAllowed = (payload: number[]) => emit('get-allowed', payload)

const getAssigned = (payload: number | null) => emit('get-assigned', payload)

const selectAuth = () =>
  nextTick(() => {
    const auth = { ...authData.value }
    if (!!props.user.staffauth) auth.pk = props.user.staffauth.pk
    else auth.pk = undefined
    emit('select-auth', auth)
  })

const dataSetup = () => {
  if (props.user && props.user?.staffauth) {
    authData.value.pk = props.user.staffauth.pk
    authData.value.contract = props.user.staffauth.contract
    authData.value.payment = props.user.staffauth.payment
    authData.value.notice = props.user.staffauth.notice
    authData.value.project_cash = props.user.staffauth.project_cash
    authData.value.project_docs = props.user.staffauth.project_docs
    authData.value.project = props.user.staffauth.project
    authData.value.project_site = props.user.staffauth.project_site
    authData.value.company_cash = props.user.staffauth.company_cash
    authData.value.company_docs = props.user.staffauth.company_docs
    authData.value.human_resource = props.user.staffauth.human_resource
    authData.value.company_settings = props.user.staffauth.company_settings
    authData.value.auth_manage = props.user.staffauth.auth_manage
  } else {
    authData.value.pk = undefined
    authData.value.contract = '0'
    authData.value.payment = '0'
    authData.value.notice = '0'
    authData.value.project_cash = '0'
    authData.value.project_docs = '0'
    authData.value.project = '0'
    authData.value.project_site = '0'
    authData.value.company_cash = '0'
    authData.value.company_docs = '0'
    authData.value.human_resource = '0'
    authData.value.company_settings = '0'
    authData.value.auth_manage = '0'
  }
}

onMounted(() => dataSetup())
onUpdated(() => dataSetup())
</script>

<template>
  <CRow>
    <CCol>
      <CRow>
        <CRow>
          <CCol>
            <h6 class="font-weight-bold">1. 본사 관리</h6>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(authData.company_cash)[0]"
                />
                본사 자금 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.company_cash"
                  :options="auths"
                  :disabled="isCoInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.company_cash)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(authData.company_docs)[0]"
                />
                본사 문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.company_docs"
                  :options="auths"
                  :disabled="isCoInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.company_docs)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(authData.human_resource)[0]"
                />
                본사 인사 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.human_resource"
                  :options="auths"
                  :disabled="isCoInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.human_resource)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(authData.company_settings)[0]"
                />
                회사 정보 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.company_settings"
                  :options="auths"
                  :disabled="isCoInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.company_settings)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(authData.auth_manage)[0]"
                />
                권한 설정 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.auth_manage"
                  :options="auths"
                  :disabled="isCoInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.auth_manage)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="6" lg="4">
            <CRow class="m-1"></CRow>
          </CCol>
        </CRow>
      </CRow>
    </CCol>
  </CRow>

  <v-divider />

  <ProjectManageAuth :user="user as User" @get-allowed="getAllowed" @get-assigned="getAssigned" />

  <v-divider />

  <CRow>
    <CCol>
      <CRow class="mb-3">
        <CRow>
          <CCol>
            <h6 class="font-weight-bold">2. 현장 관리</h6>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon icon="mdi mdi-account-arrow-left" :color="getColor(authData.contract)[0]" />
                분양 계약 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.contract"
                  :options="auths"
                  :disabled="isPrInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.contract)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon icon="mdi mdi-account-arrow-left" :color="getColor(authData.payment)[0]" />
                분양 수납 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.payment"
                  :options="auths"
                  :disabled="isPrInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.payment)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon icon="mdi mdi-account-arrow-left" :color="getColor(authData.notice)[0]" />
                고객 고지 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.notice"
                  :options="auths"
                  :disabled="isPrInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.notice)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(authData.project_cash)[0]"
                />
                현장 자금 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.project_cash"
                  :options="auths"
                  :disabled="isPrInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.project_cash)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(authData.project_docs)[0]"
                />
                현장 문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.project_docs"
                  :options="auths"
                  :disabled="isPrInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.project_docs)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon icon="mdi mdi-account-arrow-left" :color="getColor(authData.project)[0]" />
                신규 프로젝트
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.project"
                  :options="auths"
                  :disabled="isPrInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.project)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol md="6" lg="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3">
                <v-icon icon="mdi mdi-account-arrow-left" :color="getColor(authData.project)[0]" />
                사업 부지 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="authData.project_site"
                  :options="auths"
                  :disabled="isPrInActive"
                  :style="{
                    backgroundColor: isDark ? '' : getColor(authData.project_site)[1],
                  }"
                  @change="selectAuth"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </CRow>
    </CCol>
  </CRow>
</template>
