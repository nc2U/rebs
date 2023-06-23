<script lang="ts" setup>
import { ref, computed } from 'vue'
import { Succession } from '@/store/types/contract'
import { useRouter } from 'vue-router'
import { write_contract } from '@/utils/pageAuth'
import FormModal from '@/components/Modals/FormModal.vue'
import SuccessionForm from '@/views/contracts/Succession/components/SuccessionForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({ succession: { type: Object, required: true } })
const emit = defineEmits(['on-submit', 'get-succession'])

const successionFormModal = ref()
const successionAlertModal = ref()

const buttonColor = computed(() => {
  if (!props.succession.is_approval) return 'success'
  else return 'secondary'
})

const router = useRouter()

const callFormModal = () => {
  emit('get-succession', props.succession.pk)
  router.push({
    name: '권리 의무 승계',
    query: { contractor: props.succession.seller },
  })
  setTimeout(() => {
    if (write_contract.value) successionFormModal.value.callModal()
    else successionAlertModal.value.callModal()
  }, 300)
}

const onSubmit = (payload: Succession) => {
  emit('on-submit', payload)
  successionFormModal.value.close()
}
</script>

<template>
  <CTableDataCell class="text-center">
    {{ succession.apply_date }}
  </CTableDataCell>
  <CTableDataCell class="text-center">
    <router-link to="" @click="callFormModal">
      {{ succession.contract.serial_number }}
    </router-link>
  </CTableDataCell>
  <CTableDataCell class="text-center">
    {{ succession.seller.name }}
  </CTableDataCell>
  <CTableDataCell class="text-center">
    {{ succession.buyer.name }}
  </CTableDataCell>
  <CTableDataCell class="text-center">
    {{ succession.trading_date }}
  </CTableDataCell>
  <CTableDataCell class="text-primary text-center fw-bold">
    {{ succession.is_approval ? '완료' : '' }}
  </CTableDataCell>
  <CTableDataCell class="text-primary text-center fw-bold">
    {{ succession.approval_date }}
  </CTableDataCell>
  <CTableDataCell class="text-center">
    <CButton
      type="button"
      :color="buttonColor"
      size="sm"
      @click="callFormModal"
    >
      확인
    </CButton>
  </CTableDataCell>

  <FormModal ref="successionFormModal" size="lg">
    <template #header>권리 의무 승계 수정 등록</template>
    <template #default>
      <SuccessionForm
        :succession="succession"
        @on-submit="onSubmit"
        @close="successionFormModal.close()"
      />
    </template>
  </FormModal>

  <AlertModal ref="successionAlertModal" />
</template>
