<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import FormModal from '@/components/Modals/FormModal.vue'
import ReleaseForm from '@/views/contracts/Release/components/ReleaseForm.vue'

const props = defineProps({ release: { type: Object, default: null } })
const emit = defineEmits(['on-submit', 'get-release'])

const releaseFormModal = ref()

const store = useStore()
const contractor = computed(() => store.state.contract.contractor)

const getStatus = (num: string) => {
  const status = [
    { code: '0', text: '신청 취소' },
    { code: '3', text: '신청 중' },
    { code: '4', text: '처리완료' },
    { code: '5', text: '자격상실(제명)' },
  ]
  return status.filter(s => s.code === num).map(s => s.text)[0]
}
const router = useRouter()

const callFormModal = () => {
  emit('get-release', props.release.pk)
  router.push({
    name: '계약해지 관리',
    query: { contractor: props.release.contractor },
  })
  releaseFormModal.value.callModal()
}

const onSubmit = (payload: any) => {
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
  <CTableDataCell>{{ getStatus(release.status) }}</CTableDataCell>
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
  <CTableDataCell>{{ release.completion_date }}</CTableDataCell>
  <CTableDataCell>
    <CButton type="button" color="danger" size="sm" @click="callFormModal">
      확인
    </CButton>
  </CTableDataCell>

  <FormModal ref="releaseFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      계약 해지 수정 등록
    </template>
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
