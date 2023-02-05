<script lang="ts" setup="">
import { ref, computed, nextTick, onBeforeMount, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { bgLight } from '@/utils/cssMixins'
import Multiselect from '@vueform/multiselect'

const props = defineProps({ selUser: { type: Number, default: null } })
const emit = defineEmits(['select-user'])

const userId = ref<number | null>(null)

const accountStore = useAccount()
const userInfo = computed(() => accountStore.userInfo)
const getUsers = computed(() => accountStore.getUsers)

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
              :options="getUsers"
              placeholder="사용자"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
              @change="selectUser"
            />
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
</template>
