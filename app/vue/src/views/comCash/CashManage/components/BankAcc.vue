<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useComCash } from '@/store/pinia/comCash'
import type { CompanyBank } from '@/store/types/comCash'
import BankAccForm from './BankAccForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const emit = defineEmits(['on-bank-update'])

const comBankAcc = ref()
const addBankAcc = ref()

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
      <CAccordion class="mb-3">
        <CAccordionItem v-for="bank in allComBankList" :key="bank.pk" :item-key="bank.pk as number">
          <CAccordionHeader>
            {{ `${bank.alias_name}  :: ${bank.number}` }}
          </CAccordionHeader>
          <CAccordionBody class="pl-3">
            <BankAccForm :bank-acc="bank" @on-bank-update="onBankUpdate" />
          </CAccordionBody>
        </CAccordionItem>
      </CAccordion>

      <CRow>
        <CCol class="text-right">
          <v-btn prepend-icon="mdi-plus-circle" variant="text" @click="addBankAcc.callModal()">
            <template v-slot:prepend>
              <v-icon color="success"></v-icon>
            </template>
            계좌 추가
          </v-btn>
        </CCol>
      </CRow>
    </template>
    <template #footer></template>
  </AlertModal>

  <AlertModal ref="addBankAcc" size="lg">
    <template #header>계좌 추가</template>
    <template #default>
      <BankAccForm />
    </template>
  </AlertModal>
</template>
