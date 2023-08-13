<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useProCash } from '@/store/pinia/proCash'
import { type ProBankAcc } from '@/store/types/proCash'
import BankAccForm from './BankAccForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const emit = defineEmits(['on-bank-update'])

const refComBankAcc = ref()

const proCashStore = useProCash()
const allProBankAccList = computed(() => proCashStore.allProBankAccountList)

const onBankUpdate = (payload: ProBankAcc) => emit('on-bank-update', payload)

const callModal = () => refComBankAcc.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <AlertModal ref="refComBankAcc" size="lg">
    <template #header> 프로젝트 거래 계좌 관리</template>
    <template #default>
      <CAccordion>
        <CAccordionItem v-for="bank in allProBankAccList" :key="bank.pk" :item-key="bank.pk">
          <CAccordionHeader>
            {{ `${bank.alias_name}  :: ${bank.number}` }}
          </CAccordionHeader>
          <CAccordionBody class="pl-3">
            <BankAccForm :bank-acc="bank" @on-bank-update="onBankUpdate" />
          </CAccordionBody>
        </CAccordionItem>
      </CAccordion>
    </template>
    <template #footer></template>
  </AlertModal>
</template>
