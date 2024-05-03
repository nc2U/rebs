<script lang="ts" setup>
import { computed, type ComputedRef, inject, onBeforeMount, type PropType, ref } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { useWork } from '@/store/pinia/work'
import type { IssueProject } from '@/store/types/work'
import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  watchers: { type: Array as PropType<{ pk: number; username: string }[]>, default: () => [] },
})

const addUser = ref()
const refConfirmModal = ref()

const accStore = useAccount()
const getUsers = computed(() => accStore.getUsers)

const workStore = useWork()
const iProject = inject<ComputedRef<IssueProject>>('iProject')

const memberList = computed(() => {
  const members = iProject?.value ? iProject?.value?.all_members : workStore?.memberList
  return members?.map(m => m.user).filter(m => !props.watchers.map(m => m.pk).includes(m.pk))
})

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

      {{ getUsers }}

      <hr />

      {{ memberList }}
    </template>

    <template #footer>
      <CButton color="primary">추가</CButton>
    </template>
  </ConfirmModal>
</template>
