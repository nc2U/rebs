<script lang="ts" setup>
import { useContract } from '@/store/pinia/contract'
import { computed } from 'vue'

const props = defineProps({ contractor: { type: Object, default: null } })

const getStatus = (num: string) => {
  const status = [
    { code: '1', text: '청약' },
    { code: '2', text: '계약' },
    { code: '3', text: '해지신청' },
    { code: '4', text: '해지완료' },
  ]
  return status.filter(s => s.code === num).map(s => s.text)[0]
}

const contractStore = useContract()

const alertColor = computed(() => {
  let aColor = 'success'
  if (!!props.contractor.succession) aColor = 'info'
  else if (
    !!props.contractor.contractorrelease &&
    props.contractor.status >= '3'
  )
    aColor = 'danger'
  return aColor
})

const removeContractor = () => {
  contractStore.contract = null
  contractStore.contractor = null
}
</script>

<template>
  <CAlert :color="alertColor">
    <CRow>
      <CCol xs="10">
        <strong>
          <CIcon name="cilTask" />
          계약자명 :
          {{ contractor.__str__ }} :::::: 현재상태 : [{{
            getStatus(contractor.status)
          }}] {{ contractor.succession ? '--- (권리 의무 승계 진행 중!)' : '' }}
        </strong>
      </CCol>
      <CCol v-if="contractor" class="text-right">
        <router-link to="">
          <CIcon name="cilX" @click="removeContractor" />
        </router-link>
      </CCol>
    </CRow>
  </CAlert>
</template>
