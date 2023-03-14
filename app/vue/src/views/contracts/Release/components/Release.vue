<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { ContractRelease } from '@/store/types/contract'
import { useRouter } from 'vue-router'
import { numFormat, cutString } from '@/utils/baseMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import ReleaseForm from '@/views/contracts/Release/components/ReleaseForm.vue'

const props = defineProps({ release: { type: Object, default: null } })
const emit = defineEmits(['on-submit', 'get-release'])

const releaseFormModal = ref()

const contractStore = useContract()
const contractor = computed(() => contractStore.contractor)

const getStatus = (num: string) => {
  const status = [
    { code: '0', text: '신청 취소' },
    { code: '3', text: '해지 신청' },
    { code: '4', text: '해지 완료' },
    { code: '5', text: '자격 상실' },
  ]
  return status.filter(s => s.code === num).map(s => s.text)[0]
}

const textColor = computed(() => {
  if (props.release.status === '0') return 'text-primary'
  else if (props.release.status === '3') return 'text-danger'
  else return ''
})

const buttonColor = computed(() => {
  if (props.release.status === '0') return 'info'
  else if (props.release.status === '3') return 'warning'
  else return 'secondary'
})

const router = useRouter()

const callFormModal = () => {
  emit('get-release', props.release.pk)
  router.push({
    name: '계약 해지 관리',
    query: { contractor: props.release.contractor },
  })
  releaseFormModal.value.callModal()
}

const onSubmit = (payload: ContractRelease) => {
  emit('on-submit', payload)
  releaseFormModal.value.close()
}
</script>

<template>
  <CTableDataCell>
    <router-link to="" @click="callFormModal">
      {{ cutString(release.__str__, 25) }}
    </router-link>
  </CTableDataCell>
  <CTableDataCell :class="textColor">
    {{ getStatus(release.status) }}
  </CTableDataCell>
  <CTableDataCell class="text-right">
    {{ numFormat(release.refund_amount) }}
  </CTableDataCell>
  <CTableDataCell class="text-left">
    {{ release.refund_account_bank }}
  </CTableDataCell>
  <CTableDataCell class="text-left">
    {{ release.refund_account_number }}
  </CTableDataCell>
  <CTableDataCell>{{ release.refund_account_depositor }}</CTableDataCell>
  <CTableDataCell>{{ release.request_date }}</CTableDataCell>
  <CTableDataCell class="text-primary">
    <strong>{{ release.completion_date }}</strong>
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

  <FormModal ref="releaseFormModal" size="lg">
    <template #header>계약 해지 수정 등록</template>
    <template #default>
      <ReleaseForm
        :release="release"
        :contractor="contractor"
        @on-submit="onSubmit"
        @close="releaseFormModal.close()"
      />
    </template>
  </FormModal>
</template>
