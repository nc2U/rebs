<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useAccount } from '@/store/pinia/account'
import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const addUser = ref()
const refConfirmModal = ref()

const accStore = useAccount()
const getUsers = computed(() => accStore.getUsers)

const callModal = () => refConfirmModal.value.callModal()
defineExpose({ callModal })

onBeforeMount(() => accStore.fetchUsersList())
</script>

<template>
  <ConfirmModal ref="refConfirmModal">
    <template #header>업무 관람자 추가</template>

    <template #default>
      <Multiselect
        v-model="addUser"
        :options="getUsers"
        searchable
        placeholder="사용자 찾기"
        class="mb-5"
      />
    </template>

    <template #footer>
      <CButton color="primary">추가</CButton>
    </template>
  </ConfirmModal>
</template>
