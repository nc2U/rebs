<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useComCash } from '@/store/pinia/comCash'
import { CompanyBank } from '@/store/types/comCash'
import BankAccForm from './BankAccForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const emit = defineEmits(['on-bank-update'])

const comBankAcc = ref()

const comCashStore = useComCash()
const allComBankList = computed(() => comCashStore.allComBankList)

const onBankUpdate = (payload: CompanyBank) => emit('on-bank-update', payload)

const callModal = () => comBankAcc.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <AlertModal ref="comBankAcc" size="lg">
    <template #header> 본사 거래 계좌 관리</template>
    <template #default>
      <CAccordion>
        <CAccordionItem
          v-for="bank in allComBankList"
          :key="bank.pk"
          :item-key="bank.pk"
        >
          <CAccordionHeader>
            {{ `${bank.alias_name}  :: ${bank.number}` }}
          </CAccordionHeader>
          <CAccordionBody class="pl-3">
            <BankAccForm :bank-acc="bank" @onBankUpdate="onBankUpdate" />
          </CAccordionBody>
        </CAccordionItem>
      </CAccordion>
    </template>
    <template #footer></template>
  </AlertModal>
</template>
