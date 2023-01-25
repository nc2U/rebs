<script lang="ts" setup="">
import { ref, computed, nextTick, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useAccount } from '@/store/pinia/account'
import Multiselect from '@vueform/multiselect'

const emit = defineEmits(['select-user'])

const userId = ref<number | null>(null)

const store = useStore()
const isDark = computed(() => store.state.theme === 'dark')

const accountStore = useAccount()
const userInfo = computed(() => accountStore.userInfo)
const getUsers = computed(() => accountStore.getUsers)

const selectUser = () => nextTick(() => emit('select-user', userId.value))

onBeforeMount(() => {
  if (userInfo.value) userId.value = userInfo.value.pk as number
})
</script>

<template>
  <CCallout color="dark" :class="{ 'bg-light': !isDark }">
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
