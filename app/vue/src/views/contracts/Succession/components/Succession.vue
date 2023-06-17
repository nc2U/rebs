<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { Succession } from '@/store/types/contract'
import { useRouter } from 'vue-router'
import FormModal from '@/components/Modals/FormModal.vue'
import SuccessionForm from '@/views/contracts/Succession/components/SuccessionForm.vue'

const props = defineProps({ succession: { type: Object, default: null } })
const emit = defineEmits(['on-submit', 'get-succession'])

const successionFormModal = ref()

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
    query: { contractor: props.succession.contractor },
  })
  successionFormModal.value.callModal()
}

const onSubmit = (payload: Succession) => {
  emit('on-submit', payload)
  successionFormModal.value.close()
}
</script>

<template>
  <CTableDataCell>
    <router-link to="" @click="callFormModal">
      {{ succession.apply_date }}
    </router-link>
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
  <CTableDataCell>{{ succession.is_approval }}</CTableDataCell>
  <CTableDataCell>{{ succession.approval_date }}</CTableDataCell>
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
    <template #header>계약 해지 수정 등록</template>
    <template #default>
      <SuccessionForm
        :succession="succession"
        :contractor="contractor"
        @on-submit="onSubmit"
        @close="successionFormModal.close()"
      />
    </template>
  </FormModal>
</template>
