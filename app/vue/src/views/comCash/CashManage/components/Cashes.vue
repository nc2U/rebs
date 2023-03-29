<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { useAccount } from '@/store/pinia/account'
import { BankCode, CashBook } from '@/store/types/comCash'
import { write_company_cash } from '@/utils/pageAuth'
import { numFormat, cutString, diffDate } from '@/utils/baseMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import CashForm from '@/views/comCash/CashManage/components/CashForm.vue'

const props = defineProps({
  cash: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits([
  'multi-submit',
  'on-delete',
  'patch-d3-hide',
  'on-bank-update',
])

const delModal = ref()
const alertModal = ref()
const updateFormModal = ref()

const cls = ref(['text-primary', 'text-danger', 'text-info'])
const sortClass = computed(() => cls.value[props.cash.sort - 1])
const d1Class = computed(() => cls.value[props.cash.account_d1 - 1])

const store = useStore()
const dark = computed(() => store.state.theme === 'dark')
const rowColor = computed(() => {
  let color = ''
  color = dark.value ? '' : color
  color = props.cash.is_separate ? 'primary' : color
  color = props.cash.separated ? 'secondary' : color
  return color
})

const accountStore = useAccount()
const allowedPeriod = computed(
  () => accountStore.superAuth || diffDate(props.cash.deal_date) <= 30,
)

const showDetail = () => updateFormModal.value.callModal()

const multiSubmit = (payload: {
  formData: CashBook
  sepData: CashBook | null
}) => emit('multi-submit', payload)

const deleteConfirm = () => {
  if (write_company_cash.value)
    if (allowedPeriod.value) delModal.value.callModal()
    else
      alertModal.value.callModal(
        null,
        '거래일로부터 30일이 경과한 건은 삭제할 수 없습니다. 관리자에게 문의바랍니다.',
      )
  else alertModal.value.callModal()
}

const deleteObject = () => {
  emit('on-delete', { company: props.cash.company, pk: props.cash.pk })
  delModal.value.close()
}

const patchD3Hide = (payload: { pk: number; is_hide: boolean }) =>
  emit('patch-d3-hide', payload)

const onBankUpdate = (payload: BankCode) => emit('on-bank-update', payload)
</script>

<template>
  <CTableRow
    v-if="cash"
    class="text-center"
    :color="rowColor"
    :style="cash.is_separate ? 'font-weight: bold;' : ''"
  >
    <CTableDataCell>{{ cash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ cash.sort_desc }}
    </CTableDataCell>
    <CTableDataCell :class="d1Class">
      {{ cash.account_d1_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cash.account_d3_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      <span v-if="cash.content">
        {{ cutString(cash.content, 15) }}
      </span>
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      <span v-if="cash.trader">
        {{ cutString(cash.trader, 8) }}
      </span>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <span v-if="cash.bank_account_desc">
        {{ cutString(cash.bank_account_desc, 10) }}
      </span>
    </CTableDataCell>
    <CTableDataCell class="text-right" :color="dark ? '' : 'primary'">
      {{ numFormat(cash.income || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" :color="dark ? '' : 'danger'">
      {{ numFormat(cash.outlay || 0) }}
    </CTableDataCell>
    <CTableDataCell>{{ cash.evidence_desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>본사 입출금 거래 건별 수정</template>
    <template #default>
      <CashForm
        :cash="cash"
        @multi-submit="multiSubmit"
        @on-delete="deleteConfirm"
        @patchD3Hide="patchD3Hide"
        @onBankUpdate="onBankUpdate"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>

  <ConfirmModal ref="delModal">
    <template #header> 입출금 거래 정보 삭제</template>
    <template #default>
      삭제한 데이터는 복구할 수 없습니다. 해당 입출금 거래 정보를
      삭제하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
