<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { Succession } from '@/store/types/contract'
import { useRouter } from 'vue-router'
import { write_contract } from '@/utils/pageAuth'
import FormModal from '@/components/Modals/FormModal.vue'
import SuccessionForm from '@/views/contracts/Succession/components/SuccessionForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({ succession: { type: Object, default: null } })
const emit = defineEmits(['on-submit', 'get-succession'])

const successionFormModal = ref()
const successionAlertModal = ref()

const contractStore = useContract()
const contractor = computed(() => contractStore.contractor)

const buttonColor = computed(() => {
  if (!props.succession.is_approval) return 'success'
  else return 'secondary'
})

const router = useRouter()

const callFormModal = () => {
  emit('get-succession', props.succession.pk)
  router.push({
    name: '권리 의무 승계',
    query: { contractor: props.succession.seller.pk },
  })
  if (write_contract.value) successionFormModal.value.callModal()
  else successionAlertModal.value.callModal()
}

const onSubmit = (payload: Succession) => {
  emit('on-submit', payload)
  successionFormModal.value.close()
}
</script>

<template>
  <CTableDataCell>
    {{ succession.apply_date }}
  </CTableDataCell>
  <CTableDataCell>
    <router-link to="" @click="callFormModal">
      {{ succession.contract.serial_number }}
    </router-link>
  </CTableDataCell>
  <CTableDataCell>
    {{ succession.seller.name }}
  </CTableDataCell>
  <CTableDataCell>
    {{ succession.buyer.name }}
  </CTableDataCell>
  <CTableDataCell>
    {{ succession.trading_date }}
  </CTableDataCell>
  <CTableDataCell class="text-primary fw-bold">
    {{ succession.is_approval ? '완료' : '' }}
  </CTableDataCell>
  <CTableDataCell class="text-primary fw-bold">
    {{ succession.approval_date }}
  </CTableDataCell>
  <CTableDataCell>
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
        :contractor="contractor"
        @on-submit="onSubmit"
        @close="successionFormModal.close()"
      />
    </template>
  </FormModal>

  <AlertModal ref="successionAlertModal" />
</template>
