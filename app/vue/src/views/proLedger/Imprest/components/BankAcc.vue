<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useProLedger } from '@/store/pinia/proLedger'
import type { ProjectBank } from '@/store/types/proLedger.ts'
import AlertModal from '@/components/Modals/AlertModal.vue'
import BankAccForm from './BankAccForm.vue'

const emit = defineEmits(['on-bank-create', 'on-bank-update'])

const refProBankAcc = ref()
const bankAccAdd = ref(false)

const proLedgerStore = useProLedger()
const allProBankAccList = computed(() => proLedgerStore.allProBankList)

const onBankCreate = (payload: ProjectBank) => emit('on-bank-create', payload)
const onBankUpdate = (payload: ProjectBank) => emit('on-bank-update', payload)

const callModal = () => refProBankAcc.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <AlertModal ref="refProBankAcc" size="lg">
    <template #header>운영비용 거래 계좌 관리</template>
    <template #default>
      <CAccordion class="mb-3">
        <CAccordionItem v-for="bank in allProBankAccList" :key="bank.pk" :item-key="bank.pk">
          <CAccordionHeader>
            {{ `${bank.alias_name}  :: ${bank.number}` }}
          </CAccordionHeader>
          <CAccordionBody class="ps-3">
            <BankAccForm :bank-acc="bank" @on-bank-update="onBankUpdate" />
          </CAccordionBody>
        </CAccordionItem>
      </CAccordion>

      <CRow v-show="bankAccAdd">
        <CCol>
          <h5 class="p-3 bg-light">
            <v-icon icon="mdi-plus-circle" color="primary" class="me-1" />
            계좌 추가
          </h5>
          <BankAccForm @on-bank-create="onBankCreate" />
        </CCol>
      </CRow>

      <CRow>
        <CCol class="text-end">
          <v-btn
            :prepend-icon="`mdi-${!bankAccAdd ? 'plus' : 'minus'}-circle`"
            variant="text"
            @click="bankAccAdd = !bankAccAdd"
          >
            <template v-slot:prepend>
              <v-icon :color="!bankAccAdd ? 'success' : 'secondary'"></v-icon>
            </template>
            <span v-if="!bankAccAdd">계좌 추가</span>
            <span v-else>추가 취소</span>
          </v-btn>
        </CCol>
      </CRow>
    </template>
    <template #footer></template>
  </AlertModal>
</template>
