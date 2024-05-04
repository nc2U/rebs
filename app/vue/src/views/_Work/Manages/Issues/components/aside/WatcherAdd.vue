<script lang="ts" setup>
import { computed, type ComputedRef, inject, onBeforeMount, type PropType, ref, watch } from 'vue'
import { useWork } from '@/store/pinia/work'
import { useAccount } from '@/store/pinia/account'
import type { IssueProject } from '@/store/types/work'
import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  watchers: { type: Array as PropType<{ pk: number; username: string }[]>, default: () => [] },
})

const addUser = ref()
const refConfirmModal = ref()

const addUsers = ref<number[]>([])
const addMembers = ref<{ pk: number; username: string }[]>([])

const workStore = useWork()
const iProject = inject<ComputedRef<IssueProject>>('iProject')

const members = computed(() =>
  iProject?.value ? iProject?.value?.all_members : workStore?.memberList,
)

const accStore = useAccount()
const getUsers = computed(() =>
  accStore.getUsers.filter(u => !members.value?.map(m => m.pk).includes(u.value)),
) // 프로젝트 멤버외 추가 사용자 목록에서 members.value 목록 제외

const memberList = computed(() =>
  members.value?.map(m => m.user).filter(m => !props.watchers.map(m => m.pk).includes(m.pk)),
) // 즉시 추가 사용자 목록에서 members.value 목록 제외

watch(
  () => memberList.value,
  nVal => (addMembers.value = nVal ?? []),
)

const callModal = () => refConfirmModal.value.callModal()
defineExpose({ callModal })

onBeforeMount(() => {
  accStore.fetchUsersList()
  addMembers.value = memberList.value ?? []
})
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

      {{ addUsers }}

      <CFormCheck
        v-model="addUsers"
        v-for="mem in addMembers"
        :value="mem.pk"
        :id="`member-${mem.pk}`"
        :label="mem.username"
        :key="mem.pk"
      />
    </template>

    <template #footer>
      <CButton color="primary">추가</CButton>
    </template>
  </ConfirmModal>
</template>
