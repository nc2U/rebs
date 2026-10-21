<script lang="ts" setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRawTransaction } from '@/store/pinia/rawTransaction'
import { useCompany } from '@/store/pinia/company'
import { useProject } from '@/store/pinia/project'
import type { BankDiscoveredAccount, BatchLinkAccountItem } from '@/store/types/rawTransaction'

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    companyId?: number | null
    projectId?: number | null
  }>(),
  {
    companyId: null,
    projectId: null,
  },
)

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'registered'): void
}>()

const rawStore = useRawTransaction()
const comStore = useCompany()
const projectStore = useProject()

// 단계 (1: 인증서/계정 등록, 2: 발견된 계좌 매핑)
const currentStep = ref<number>(1)

// 은행 목록 정의
const bankOptions = [
  { title: 'KB국민은행 (0004)', value: '0004' },
  { title: '신한은행 (0088)', value: '0088' },
  { title: '우리은행 (0020)', value: '0020' },
  { title: '하나은행 (0081)', value: '0081' },
  { title: 'IBK기업은행 (0003)', value: '0003' },
  { title: 'NH농협은행 / 지역농축협·단위농협 (0011)', value: '0011' },

  { title: 'SC제일은행 (0023)', value: '0023' },
  { title: '한국씨티은행 (0027)', value: '0027' },
  { title: 'KDB산업은행 (0002)', value: '0002' },
  { title: '카카오뱅크 (0090)', value: '0090' },
  { title: '케이뱅크 (0089)', value: '0089' },
  { title: '토스뱅크 (0092)', value: '0092' },
  { title: 'iM뱅크/대구 (0031)', value: '0031' },
  { title: 'BNK부산은행 (0032)', value: '0032' },
  { title: '광주은행 (0034)', value: '0034' },
  { title: '전북은행 (0037)', value: '0037' },
  { title: 'BNK경남은행 (0039)', value: '0039' },
  { title: '우체국 (0071)', value: '0071' },
  { title: 'Sh수협은행 (0007)', value: '0007' },
  { title: '새마을금고 (0045)', value: '0045' },
  { title: '신협 (0048)', value: '0048' },
]

// Step 1 Form State
const selectedBank = ref<string>('')
const loginType = ref<'0' | '1' | 'fast'>('0') // '0': 공동인증서, '1': ID/PW, 'fast': 신탁사/조합 빠른조회
const certFormat = ref<'single' | 'split'>('single') // 'single': .pfx/.p12/.pt2 단일 파일, 'split': der + key 2개 파일
const singleCertFile = ref<File | null>(null)
const loginId = ref<string>('')
const password = ref<string>('')
const derFile = ref<File | null>(null)
const keyFile = ref<File | null>(null)

// 신탁사/조합 빠른조회 전용 Form State
const fastAccount = ref<string>('')
const fastBizNumber = ref<string>('')
const fastPassword = ref<string>('')
const fastAlias = ref<string>('')
const fastHolder = ref<string>('')
const fastTargetType = ref<'project' | 'company'>(props.projectId ? 'project' : 'company')
const fastProjectId = ref<number | null>(props.projectId || null)
const fastCompanyId = ref<number | null>(props.companyId || null)
const fastIsImprest = ref<boolean>(false)

const isRegistering = ref<boolean>(false)

// Step 2 Form State
const connectedId = ref<string>('')
const discoveredAccounts = ref<BankDiscoveredAccount[]>([])
const selectedAccountIndexes = ref<number[]>([])

interface AccountLinkState {
  target_type: 'company' | 'project'
  company_id: number | null
  project_id: number | null
  is_imprest: boolean
  existing_account_id: number | null
  alias_name: string
}
const linkStates = ref<Record<number, AccountLinkState>>({})
const isLinking = ref<boolean>(false)

// 회사 목록 & 프로젝트 목록 옵션
const companyOptions = computed(() => {
  return comStore.companyList.map((c: any) => ({
    title: c.name,
    value: c.pk,
  }))
})

const projectOptions = computed(() => {
  return projectStore.projectList.map((p: any) => ({
    title: p.name,
    value: p.pk,
  }))
})

// Step 1 유효성
const isStep1Valid = computed(() => {
  if (!selectedBank.value) return false
  if (loginType.value === 'fast') {
    return (
      fastAccount.value.trim().length >= 8 &&
      fastBizNumber.value.replace(/[^0-9]/g, '').length >= 10 &&
      fastPassword.value.trim().length >= 4 &&
      ((fastTargetType.value === 'project' && !!fastProjectId.value) ||
        (fastTargetType.value === 'company' && !!fastCompanyId.value))
    )
  }
  if (!password.value) return false
  if (loginType.value === '0') {
    if (certFormat.value === 'single') {
      return singleCertFile.value !== null
    } else {
      return derFile.value !== null && keyFile.value !== null
    }
  } else {
    return loginId.value.trim().length > 0
  }
})

// 신탁사/조합 빠른조회 계좌 직접 연동 실행
const handleRegisterFast = async () => {
  if (!isStep1Valid.value) return
  isRegistering.value = true

  try {
    await rawStore.registerFastAccount({
      bank_code: selectedBank.value,
      account_number: fastAccount.value.trim(),
      business_number: fastBizNumber.value.replace(/[^0-9]/g, '').trim(),
      account_password: fastPassword.value.trim(),
      target_type: fastTargetType.value,
      project_id: fastTargetType.value === 'project' ? fastProjectId.value : null,
      company_id: fastTargetType.value === 'company' ? fastCompanyId.value : null,
      alias_name: fastAlias.value.trim() || undefined,
      holder: fastHolder.value.trim() || undefined,
      is_imprest: fastTargetType.value === 'project' ? fastIsImprest.value : false,
    })

    emit('registered')
    emit('update:modelValue', false)
  } finally {
    isRegistering.value = false
  }
}

// Step 1: 인증서/계정 등록 실행
const handleRegisterCertificate = async () => {
  if (loginType.value === 'fast') {
    return handleRegisterFast()
  }
  if (!isStep1Valid.value) return
  isRegistering.value = true

  try {
    const formData = new FormData()
    formData.append('bank_code', selectedBank.value)
    formData.append('login_type', loginType.value)
    formData.append('password', password.value)

    if (loginType.value === '0') {
      if (certFormat.value === 'single') {
        if (singleCertFile.value) formData.append('cert_file', singleCertFile.value)
      } else {
        if (derFile.value) formData.append('der_file', derFile.value)
        if (keyFile.value) formData.append('key_file', keyFile.value)
      }
    } else {
      formData.append('id', loginId.value)
    }

    const res = await rawStore.registerCertificate(formData)
    connectedId.value = res.connected_id
    discoveredAccounts.value = res.accounts || []

    // Step 2 링크 상태 초기화
    linkStates.value = {}
    selectedAccountIndexes.value = []

    discoveredAccounts.value.forEach((acc, idx) => {
      // 이미 등록된 계좌가 아닌 경우 기본 선택
      if (!acc.is_already_registered) {
        selectedAccountIndexes.value.push(idx)
      }

      // 기본 타겟 설정
      let target_type: 'company' | 'project' = 'project'
      let target_company: number | null = props.companyId
      let target_project: number | null = props.projectId
      let is_imprest = false

      if (acc.matched_type === 'company') {
        target_type = 'company'
        target_company =
          acc.company_id || props.companyId || (companyOptions.value[0]?.value ?? null)
      } else if (acc.matched_type === 'project') {
        target_type = 'project'
        target_project =
          acc.project_id || props.projectId || (projectOptions.value[0]?.value ?? null)
        is_imprest = acc.is_imprest
      } else {
        // 미매칭 시 props의 컨텍스트 우선
        if (props.companyId && !props.projectId) {
          target_type = 'company'
          target_company = props.companyId
        } else if (props.projectId) {
          target_type = 'project'
          target_project = props.projectId
        } else {
          target_type = 'company'
          target_company = companyOptions.value[0]?.value ?? null
        }
      }

      linkStates.value[idx] = {
        target_type,
        company_id: target_company,
        project_id: target_project,
        is_imprest,
        existing_account_id: acc.matched_account_id,
        alias_name:
          acc.matched_account_alias || acc.account_name || `계좌 ${acc.account_number.slice(-4)}`,
      }
    })

    currentStep.value = 2
  } catch (e) {
    // handled by store
  } finally {
    isRegistering.value = false
  }
}

// Step 2: 선택된 계좌 일괄 연동 저장
const handleBatchLink = async () => {
  if (selectedAccountIndexes.value.length === 0) return
  isLinking.value = true

  try {
    const items: BatchLinkAccountItem[] = selectedAccountIndexes.value.map(idx => {
      const acc = discoveredAccounts.value[idx]
      const state = linkStates.value[idx]

      return {
        account_number: acc.account_number,
        account_name: acc.account_name,
        holder: acc.holder,
        target_type: state.target_type,
        company_id: state.target_type === 'company' ? state.company_id : undefined,
        project_id: state.target_type === 'project' ? state.project_id : undefined,
        is_imprest: state.target_type === 'project' ? state.is_imprest : false,
        existing_account_id: state.existing_account_id,
        alias_name: state.alias_name,
      }
    })

    await rawStore.batchLinkCredentials({
      connected_id: connectedId.value,
      bank_code: selectedBank.value,
      items,
    })

    emit('registered')
    emit('update:modelValue', false)
  } catch (e) {
    // handled by store
  } finally {
    isLinking.value = false
  }
}

// 폼 초기화
const resetForm = () => {
  currentStep.value = 1
  selectedBank.value = ''
  loginType.value = '0'
  certFormat.value = 'single'
  singleCertFile.value = null
  loginId.value = ''
  password.value = ''
  derFile.value = null
  keyFile.value = null
  connectedId.value = ''
  discoveredAccounts.value = []
  selectedAccountIndexes.value = []
  linkStates.value = {}
}

watch(
  () => props.modelValue,
  val => {
    if (val) {
      resetForm()
      if (comStore.companyList.length === 0) comStore.fetchCompanyList()
      if (projectStore.projectList.length === 0) projectStore.fetchProjectList()
    }
  },
)

onMounted(() => {
  if (comStore.companyList.length === 0) comStore.fetchCompanyList()
  if (projectStore.projectList.length === 0) projectStore.fetchProjectList()
})
</script>

<template>
  <v-dialog
    :model-value="props.modelValue"
    max-width="1050"
    scrollable
    persistent
    @update:model-value="emit('update:modelValue', $event)"
  >
    <v-card class="pa-2 bg-more-white text-body">
      <!-- 헤더 -->
      <v-card-title class="d-flex align-center justify-space-between pb-3 border-b">
        <div class="d-flex align-center">
          <v-icon color="primary" class="mr-2">mdi-shield-key-outline</v-icon>
          <span class="text-h6 font-weight-bold">
            은행 계좌 자동 연동 (공동인증서 / 계정 등록 마법사)
          </span>
        </div>
        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          @click="emit('update:modelValue', false)"
        />
      </v-card-title>

      <!-- 단계 안내 배너 -->
      <v-card-text class="pt-4 pb-2">
        <v-row dense class="mb-2">
          <v-col cols="12">
            <v-sheet
              rounded="lg"
              class="d-flex align-center justify-space-around py-3 px-4 bg-more-light border"
            >
              <div class="d-flex align-center ga-2">
                <v-avatar
                  size="28"
                  :color="currentStep === 1 ? 'primary' : 'grey-lighten-1'"
                  class="text-white font-weight-bold"
                >
                  1
                </v-avatar>
                <div>
                  <div
                    class="font-weight-bold"
                    :class="currentStep === 1 ? 'text-primary' : 'text-grey'"
                  >
                    은행 및 인증서 등록
                  </div>
                  <div class="text-caption text-grey">인증서 업로드 및 Connected ID 발급</div>
                </div>
              </div>

              <v-icon color="grey-lighten-1">mdi-chevron-right</v-icon>

              <div class="d-flex align-center ga-2">
                <v-avatar
                  size="28"
                  :color="currentStep === 2 ? 'primary' : 'grey-lighten-1'"
                  class="text-white font-weight-bold"
                >
                  2
                </v-avatar>
                <div>
                  <div
                    class="font-weight-bold"
                    :class="currentStep === 2 ? 'text-primary' : 'text-grey'"
                  >
                    보유 계좌 확인 및 매핑
                  </div>
                  <div class="text-caption text-grey">발견된 계좌를 본사/프로젝트에 일괄 연결</div>
                </div>
              </div>
            </v-sheet>
          </v-col>
        </v-row>

        <!-- ============================================== -->
        <!-- STEP 1: 은행 및 인증서 등록 Form -->
        <!-- ============================================== -->
        <div v-if="currentStep === 1" class="py-2">
          <v-alert
            type="info"
            variant="tonal"
            density="compact"
            icon="mdi-shield-check"
            class="mb-4 text-caption"
          >
            <strong>보안 안내:</strong> 업로드하신 공동인증서 파일 및 비밀번호는 서버에 절대 영구
            저장되지 않으며, 메모리 상에서 코드에프(CODEF) 인증 식별키(Connected ID) 발급 요청 1회에
            한해 사용된 후 즉시 안전하게 소멸됩니다.
          </v-alert>

          <v-row dense>
            <!-- 거래 은행 선택 -->
            <v-col cols="12" md="5">
              <v-select
                v-model="selectedBank"
                :items="bankOptions"
                label="연동할 거래 은행 선택 *"
                placeholder="인증서가 등록된 은행 선택"
                clearable
                density="compact"
                variant="outlined"
                prepend-inner-icon="mdi-bank"
                :hint="selectedBank === '0011' ? '※ NH농협은행 및 각 지역 농·축협(단위농협) 계좌는 0011로 통합 조회됩니다.' : undefined"
                :persistent-hint="selectedBank === '0011'"
              />
            </v-col>

            <!-- 로그인/연동 방식 선택 (공동인증서 vs ID/PW vs 신탁사 빠른조회) -->
            <v-col cols="12" md="7">
              <v-btn-toggle
                v-model="loginType"
                mandatory
                color="primary"
                density="compact"
                variant="outlined"
                class="w-100 text-body"
              >
                <v-btn value="0" size="small" class="flex-grow-1" prepend-icon="mdi-certificate">
                  법인 공동인증서
                </v-btn>
                <v-btn value="fast" size="small" class="flex-grow-1" prepend-icon="mdi-flash">
                  신탁/조합 빠른조회
                </v-btn>
                <v-btn value="1" size="small" class="flex-grow-1" prepend-icon="mdi-account-key">
                  인터넷뱅킹 ID
                </v-btn>
              </v-btn-toggle>
            </v-col>
          </v-row>

          <!-- ============================================== -->
          <!-- A. 공동인증서 업로드 영역 -->
          <!-- ============================================== -->
          <div v-if="loginType === '0'" class="mt-2 pa-3 bg-more-light border rounded">
            <div class="d-flex align-center justify-space-between mb-2 flex-wrap ga-2">
              <div class="text-subtitle-2 font-weight-bold d-flex align-center">
                <v-icon size="18" color="primary" class="mr-1">mdi-file-certificate-outline</v-icon>
                공동인증서 파일 업로드
              </div>
              <v-btn-toggle
                v-model="certFormat"
                mandatory
                density="compact"
                variant="outlined"
                color="primary"
                class="text-body"
              >
                <v-btn value="single" size="x-small"> 통합 파일 (.pfx / .p12 / .pt2) 추천 </v-btn>
                <v-btn value="split" size="x-small"> 폴더 분리형 (.der + .key) </v-btn>
              </v-btn-toggle>
            </div>

            <!-- 단일 통합 파일 업로드 (.pfx, .p12, .pt2 등) -->
            <div v-if="certFormat === 'single'">
              <div class="text-caption text-grey-darken-1 mb-2">
                💡 은행 인터넷뱅킹 또는 인증센터에서 '인증서 내보내기/백업'으로 저장한 단일 통합
                파일(<strong>.pfx</strong>, <strong>.p12</strong>, 또는 <strong>.pt2</strong>) 1개만
                선택해 주세요.
              </div>
              <v-file-input
                v-model="singleCertFile"
                accept=".pfx,.p12,.pt2"
                label="통합 인증서 파일 (.pfx / .p12 / .pt2) *"
                density="compact"
                variant="outlined"
                show-size
                prepend-icon=""
                prepend-inner-icon="mdi-file-lock-outline"
                placeholder="인증서 백업 파일 선택"
              />
            </div>

            <!-- 폴더 분리형 2개 파일 업로드 (.der + .key) -->
            <div v-else>
              <div class="text-caption text-grey-darken-1 mb-2">
                💡 PC의 <code>C:\Users\사용자\AppData\LocalLow\NPKI</code> 또는 USB 이동식 디스크의
                은행용 인증서 폴더에서 <code>signCert.der</code> 파일과
                <code>signPri.key</code> 파일을 각각 선택해 주세요.
              </div>
              <v-row dense>
                <v-col cols="12" sm="6">
                  <v-file-input
                    v-model="derFile"
                    accept=".der"
                    label="인증서 파일 (signCert.der) *"
                    density="compact"
                    variant="outlined"
                    show-size
                    prepend-icon=""
                    prepend-inner-icon="mdi-file-document-outline"
                  />
                </v-col>
                <v-col cols="12" sm="6">
                  <v-file-input
                    v-model="keyFile"
                    accept=".key"
                    label="인증서 개인키 (signPri.key) *"
                    density="compact"
                    variant="outlined"
                    show-size
                    prepend-icon=""
                    prepend-inner-icon="mdi-key-variant"
                  />
                </v-col>
              </v-row>
            </div>
          </div>

          <!-- ============================================== -->
          <!-- B. 신탁사/조합 빠른조회 폼 (인증서 불필요) -->
          <!-- ============================================== -->
          <div
            v-else-if="loginType === 'fast'"
            class="mt-2 pa-3 bg-more-light border border-teal rounded"
          >
            <div class="d-flex align-center mb-2">
              <v-icon size="20" color="teal-darken-2" class="mr-1">mdi-bank-check</v-icon>
              <span class="text-subtitle-2 font-weight-bold text-teal-darken-3">
                신탁사 및 조합 전용 빠른조회(스피드조회) 계좌 연동
              </span>
            </div>
            <div class="text-caption text-grey-darken-2 mb-3">
              💡 신탁사 신탁계좌나 조합 계좌처럼
              <strong>공동인증서를 직접 보관할 수 없는 계좌</strong>를 위한 전용 방식입니다.<br />
              신탁사 또는 조합이 해당 은행 인터넷뱅킹에 '빠른조회/스피드조회 서비스'로 등록한 정보를
              입력하시면 <strong>인증서 없이 즉시 실시간 입출금 내역을 수집</strong>합니다.
            </div>

            <v-row dense>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="fastAccount"
                  label="계좌번호 *"
                  placeholder="'-' 없이 숫자만 입력"
                  density="compact"
                  variant="outlined"
                  prepend-inner-icon="mdi-numeric"
                  hide-details="auto"
                  class="mb-2"
                />
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="fastBizNumber"
                  label="신탁사/조합 사업자등록번호 (10자리) *"
                  placeholder="예: 1234567890"
                  density="compact"
                  variant="outlined"
                  prepend-inner-icon="mdi-domain"
                  hide-details="auto"
                  class="mb-2"
                />
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="fastPassword"
                  type="password"
                  label="통장 비밀번호 또는 빠른조회 비밀번호 *"
                  placeholder="비밀번호 4자리 이상"
                  density="compact"
                  variant="outlined"
                  prepend-inner-icon="mdi-lock-outline"
                  hide-details="auto"
                  class="mb-2"
                />
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="fastAlias"
                  label="계좌 별칭 (선택)"
                  placeholder="예: 무궁화신탁 수납계좌 / A구역 조합통장"
                  density="compact"
                  variant="outlined"
                  prepend-inner-icon="mdi-tag-outline"
                  hide-details="auto"
                  class="mb-2"
                />
              </v-col>

              <!-- 귀속 구분 (프로젝트 vs 본사) -->
              <v-col cols="12" sm="4">
                <v-select
                  v-model="fastTargetType"
                  :items="[
                    { title: '프로젝트 계좌 (추천)', value: 'project' },
                    { title: '본사 관리 계좌', value: 'company' },
                  ]"
                  label="귀속 구분 *"
                  density="compact"
                  variant="outlined"
                  hide-details="auto"
                />
              </v-col>

              <v-col v-if="fastTargetType === 'project'" cols="12" sm="5">
                <v-select
                  v-model="fastProjectId"
                  :items="projectOptions"
                  label="연결할 프로젝트 선택 *"
                  density="compact"
                  variant="outlined"
                  hide-details="auto"
                />
              </v-col>

              <v-col v-if="fastTargetType === 'company'" cols="12" sm="5">
                <v-select
                  v-model="fastCompanyId"
                  :items="companyOptions"
                  label="연결할 회사 선택 *"
                  density="compact"
                  variant="outlined"
                  hide-details="auto"
                />
              </v-col>

              <v-col
                v-if="fastTargetType === 'project'"
                cols="12"
                sm="3"
                class="d-flex align-center"
              >
                <v-checkbox
                  v-model="fastIsImprest"
                  label="운영비(전도금) 계좌"
                  color="teal"
                  density="compact"
                  hide-details
                />
              </v-col>
            </v-row>
          </div>

          <!-- ============================================== -->
          <!-- C. 인터넷뱅킹 아이디 영역 -->
          <!-- ============================================== -->
          <v-row v-else-if="loginType === '1'" dense class="mt-4">
            <v-col cols="12">
              <v-text-field
                v-model="loginId"
                label="인터넷뱅킹 사용자 ID *"
                density="compact"
                variant="outlined"
                prepend-inner-icon="mdi-account"
                placeholder="은행 기업인터넷뱅킹 아이디"
              />
            </v-col>
          </v-row>

          <!-- 공동인증서 / ID 로그인일 때만 비밀번호 공통 입력 필드 표시 -->
          <v-row v-if="loginType !== 'fast'" dense class="mt-2">
            <v-col cols="12">
              <v-text-field
                v-model="password"
                type="password"
                :label="
                  loginType === '0' ? '공동인증서 비밀번호 *' : '인터넷뱅킹 로그인 비밀번호 *'
                "
                density="compact"
                variant="outlined"
                prepend-inner-icon="mdi-lock-outline"
                placeholder="비밀번호 입력"
                @keyup.enter="handleRegisterCertificate"
              />
            </v-col>
          </v-row>
        </div>

        <!-- ============================================== -->
        <!-- STEP 2: 발견된 계좌 확인 및 매핑 테이블 -->
        <!-- ============================================== -->
        <div v-else class="py-2">
          <v-alert
            type="success"
            variant="tonal"
            density="compact"
            icon="mdi-check-decagram"
            class="mb-3 text-caption"
          >
            <strong>계정 연동 성공!</strong> 코드에프(CODEF)로부터 커넥티드 ID가 정상 발급되었으며,
            해당 은행에서 <strong>총 {{ discoveredAccounts.length }}개</strong>의 계좌를
            확인했습니다. 시스템에 연동할 계좌를 선택하고 본사/프로젝트를 지정해 주세요.
          </v-alert>

          <v-table density="compact" hover class="border">
            <thead class="bg-grey-lighten-4">
              <tr>
                <th class="text-center" style="width: 50px">선택</th>
                <th class="text-left" style="width: 180px">계좌번호</th>
                <th class="text-left" style="width: 180px">예금주 / 상품명</th>
                <th class="text-left" style="width: 140px">IBS 연동 구분</th>
                <th class="text-left">연결 대상 (회사 / 프로젝트)</th>
                <th class="text-center" style="width: 120px">상태</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="discoveredAccounts.length === 0">
                <td colspan="6" class="text-center py-6 text-grey">발견된 계좌가 없습니다.</td>
              </tr>
              <tr
                v-for="(acc, idx) in discoveredAccounts"
                :key="acc.account_number"
                :class="{ 'bg-grey-lighten-5': acc.is_already_registered }"
              >
                <!-- 체크박스 -->
                <td class="text-center">
                  <v-checkbox-btn
                    v-model="selectedAccountIndexes"
                    :value="idx"
                    density="compact"
                    :disabled="acc.is_already_registered"
                  />
                </td>

                <!-- 계좌번호 -->
                <td>
                  <div class="font-weight-bold font-monospace">{{ acc.account_number }}</div>
                  <div v-if="acc.balance !== null" class="text-caption text-grey">
                    잔액: {{ Number(acc.balance).toLocaleString() }}원
                  </div>
                </td>

                <!-- 예금주 / 상품명 -->
                <td>
                  <div class="font-weight-medium">{{ acc.holder || '-' }}</div>
                  <div class="text-caption text-grey text-truncate" style="max-width: 170px">
                    {{ acc.account_name || '보통예금' }}
                  </div>
                </td>

                <!-- IBS 구분 (본사 vs 프로젝트) -->
                <td>
                  <v-select
                    v-model="linkStates[idx].target_type"
                    :items="[
                      { title: '본사 계좌', value: 'company' },
                      { title: '프로젝트 계좌', value: 'project' },
                    ]"
                    density="compact"
                    variant="outlined"
                    hide-details
                    :disabled="acc.is_already_registered || !selectedAccountIndexes.includes(idx)"
                    style="font-size: 12px"
                  />
                </td>

                <!-- 연결 대상 (회사 또는 프로젝트) -->
                <td>
                  <div
                    v-if="linkStates[idx].target_type === 'company'"
                    class="d-flex align-center ga-2"
                  >
                    <v-select
                      v-model="linkStates[idx].company_id"
                      :items="companyOptions"
                      label="회사 선택"
                      density="compact"
                      variant="outlined"
                      hide-details
                      :disabled="acc.is_already_registered || !selectedAccountIndexes.includes(idx)"
                      style="min-width: 180px; font-size: 12px"
                    />
                  </div>
                  <div v-else class="d-flex align-center ga-2 flex-wrap">
                    <v-select
                      v-model="linkStates[idx].project_id"
                      :items="projectOptions"
                      label="프로젝트 선택"
                      density="compact"
                      variant="outlined"
                      hide-details
                      :disabled="acc.is_already_registered || !selectedAccountIndexes.includes(idx)"
                      style="min-width: 180px; font-size: 12px"
                    />
                    <v-checkbox
                      v-model="linkStates[idx].is_imprest"
                      label="운영비 전도금"
                      density="compact"
                      hide-details
                      color="teal"
                      :disabled="acc.is_already_registered || !selectedAccountIndexes.includes(idx)"
                      class="text-caption"
                    />
                  </div>
                </td>

                <!-- 매칭 상태 뱃지 -->
                <td class="text-center">
                  <v-chip
                    v-if="acc.is_already_registered"
                    size="x-small"
                    color="grey"
                    variant="flat"
                  >
                    연동 완료됨
                  </v-chip>
                  <v-chip
                    v-else-if="acc.matched_type"
                    size="x-small"
                    color="success"
                    variant="tonal"
                  >
                    기존 계좌 일치
                  </v-chip>
                  <v-chip v-else size="x-small" color="info" variant="outlined"> 신규 생성 </v-chip>
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>
      </v-card-text>

      <!-- 모달 푸터 버튼 -->
      <v-card-actions class="d-flex justify-space-between pt-2 px-3 border-t">
        <div>
          <v-btn
            v-if="currentStep === 2"
            variant="text"
            prepend-icon="mdi-arrow-left"
            @click="currentStep = 1"
          >
            이전 단계 (인증서 변경)
          </v-btn>
        </div>

        <div class="d-flex ga-2">
          <!-- Step 1 버튼 -->
          <v-btn
            v-if="currentStep === 1"
            :color="loginType === 'fast' ? 'teal' : 'primary'"
            variant="elevated"
            :prepend-icon="loginType === 'fast' ? 'mdi-flash' : 'mdi-magnify-scan'"
            :loading="isRegistering"
            :disabled="!isStep1Valid"
            @click="handleRegisterCertificate"
          >
            {{ loginType === 'fast' ? '신탁/빠른조회 계좌 즉시 연동' : '인증서 등록 및 계좌 탐색' }}
          </v-btn>

          <!-- Step 2 버튼 -->
          <v-btn
            v-else
            color="success"
            variant="flat"
            prepend-icon="mdi-check-all"
            :loading="isLinking"
            :disabled="selectedAccountIndexes.length === 0"
            @click="handleBatchLink"
          >
            선택 계좌 연동 완료 ({{ selectedAccountIndexes.length }}건)
          </v-btn>

          <v-btn variant="outlined" color="grey" @click="emit('update:modelValue', false)">
            닫기
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
