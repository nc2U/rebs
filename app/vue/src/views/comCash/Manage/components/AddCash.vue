<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import FormModal from '@/components/Modals/FormModal.vue'
import CashForm from '@/views/comCash/Manage/components/CashForm.vue'

const emit = defineEmits(['on-create'])

const createFormModal = ref()
const createAlertModal = ref()

const accountStore = useAccount()

const pageManageAuth = computed(
  () =>
    accountStore.superAuth ||
    (accountStore.staffAuth && accountStore.staffAuth.company_cash === '2'),
)

const createConfirm = () => {
  if (pageManageAuth.value) createFormModal.value.callModal()
  else createAlertModal.value.callModal()
}

const createObject = (payload: any) => {
  emit('on-create', payload)
  createFormModal.value.visible = false
}
</script>

<template>
  <CAlert color="secondary" class="text-right">
    <CButton color="primary" @click="createConfirm">신규등록</CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      입출금 거래 건별 등록
    </template>
    <template #default>
      <CashForm @on-submit="createObject" @close="createFormModal.close()" />
    </template>
  </FormModal>

  <AlertModal ref="createAlertModal" />
</template>
