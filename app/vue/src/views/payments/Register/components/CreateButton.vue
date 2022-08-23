<script lang="ts" setup>
import { ref, computed } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import PaymentForm from '@/views/payments/Register/components/PaymentForm.vue'

const props = defineProps({ contract: { type: Object, default: null } })
const emit = defineEmits(['on-create'])

const createFormModal = ref()

const btnActive = computed(() => !props.contract)

const showDetail = () => createFormModal.value.callModal()

const createObject = (payload: any) => {
  emit('on-create', payload)
  createFormModal.value.close()
}
</script>

<template>
  <CAlert color="secondary" class="text-right">
    <CButton
      type="button"
      color="primary"
      :disabled="btnActive"
      @click="showDetail"
    >
      신규납부 등록
    </CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      건별 수납 관리 [신규 납부등록]
    </template>
    <template #default>
      <PaymentForm
        :contract="contract"
        @on-submit="createObject"
        @close="createFormModal.close()"
      />
    </template>
  </FormModal>
</template>
