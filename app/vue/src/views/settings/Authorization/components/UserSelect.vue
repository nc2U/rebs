<script lang="ts" setup="">
import { ref, computed, nextTick, onBeforeMount, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { bgLight } from '@/utils/cssMixins'
import Multiselect from '@vueform/multiselect'

const props = defineProps({
  selUser: { type: Number, default: null },
  isStaff: { type: Boolean, default: false },
  isProjectStaff: { type: Boolean, default: false },
})
const emit = defineEmits(['select-user', 'change-staff', 'change-pro-staff'])

const userId = ref<number | null>(null)
const staff = ref(false)
const projectStaff = ref(false)

const accountStore = useAccount()
const userInfo = computed(() => accountStore.userInfo)
const getUsers = computed(() => accountStore.getUsers)

const allowGetUsers = computed(() =>
  userInfo.value?.is_superuser
    ? getUsers.value
    : getUsers.value.filter(u => u.value === userInfo.value?.pk),
)

const selectUser = () => nextTick(() => emit('select-user', userId.value))

onBeforeMount(() => {
  if (userInfo.value) userId.value = userInfo.value.pk as number
})

watch(
  () => props.selUser,
  newVal => {
    if (!!newVal) userId.value = newVal
    else userId.value = null
  },
)

watch(
  () => props.isStaff,
  nVal => (staff.value = nVal),
)

watch(
  () => props.isProjectStaff,
  nVal => (projectStaff.value = nVal),
)

const changeStaff = () =>
  nextTick(() => {
    projectStaff.value = !staff.value
    emit('change-staff', staff.value)
  })

const changeProStaff = () =>
  nextTick(() => {
    staff.value = !projectStaff.value
    emit('change-pro-staff', projectStaff.value)
  })

onBeforeMount(() => {
  if (props.isStaff) staff.value = props.isStaff
  if (props.isProjectStaff) projectStaff.value = props.isProjectStaff
})
</script>

<template>
  <CCallout color="dark" :class="bgLight">
    <CRow>
      <CCol md="10" lg="8" xl="6">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label"> 사용자 선택</CFormLabel>
          <CCol>
            <Multiselect
              v-model="userId"
              :options="allowGetUsers"
              placeholder="사용자"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter', 'tab']"
              searchable
              @change="selectUser"
            />
          </CCol>
        </CRow>
      </CCol>
      <CCol class="pt-2">
        <CFormSwitch
          v-model="staff"
          label="본사 관리자로 승인(프로젝트 관리 가능)"
          @change="changeStaff"
          id="is_staff"
        />
      </CCol>
      <CCol class="pt-2">
        <CFormSwitch
          v-model="projectStaff"
          label="프로젝트 관리자로 승인"
          @change="changeProStaff"
          id="is_project_staff"
        />
      </CCol>
    </CRow>
  </CCallout>
</template>
