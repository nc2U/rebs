<script lang="ts" setup>
import { computed, ref } from 'vue'
import { AlertSecondary } from '@/utils/cssMixins.ts'
import { usePerms } from '@/composables/usePerms.ts'
import { type PromotionPolicy } from '@/store/types/company.ts'
import PolicyForm from './PolicyForm.vue'
import FormModal from '@/components/Modals/FormModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps<{ company?: string | null }>()
const emit = defineEmits<{
  (e: 'multi-submit', payload: PromotionPolicy): void
}>()

const refFormModal = ref()
const refAlertModal = ref()

const { canGlobal, PERM } = usePerms()
const canHrWorkCreate = computed(() => canGlobal(PERM.HQ_HR_WORK_CREATE))

const createConfirm = () => {
  if (canHrWorkCreate.value) refFormModal.value.callModal()
  else refAlertModal.value.callModal()
}
const multiSubmit = (payload: PromotionPolicy) => emit('multi-submit', payload)
</script>

<template>
  <CAlert :color="AlertSecondary" class="text-end">
    <v-btn color="primary" variant="flat" :disabled="!company" @click="createConfirm">
      승급 정책 신규 등록
    </v-btn>
  </CAlert>

  <FormModal ref="refFormModal" size="lg">
    <template #header>승급 정책 신규 등록</template>
    <template #default>
      <PolicyForm :company="company" @multi-submit="multiSubmit" @close="refFormModal.close()" />
    </template>
  </FormModal>

  <AlertModal ref="refAlertModal" />
</template>
