<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { CashBook } from '@/store/types/comCash'
import { write_company_cash } from '@/utils/pageAuth'
import { numFormat, cutString, diffDate } from '@/utils/baseMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import CashForm from '@/views/comCash/Manage/components/CashForm.vue'

const props = defineProps({
  cash: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const delModal = ref()
const alertModal = ref()
const updateFormModal = ref()

const cls = ref(['text-primary', 'text-danger', 'text-info'])
const sortClass = computed(() => cls.value[props.cash.sort - 1])
const d1Class = computed(() => cls.value[props.cash.account_d1 - 1])

const accountStore = useAccount()

const pageManageAuth = computed(() => write_company_cash)

const allowedPeriod = computed(
  () => accountStore.superAuth || diffDate(props.cash.deal_date) <= 30,
)

const showDetail = () => {
  updateFormModal.value.callModal()
}

const multiSubmit = (payload: {
  formData: CashBook
  sepData: CashBook | null
}) => {
  emit('multi-submit', payload)
  updateFormModal.value.visible = false
}

const deleteConfirm = () => {
  if (pageManageAuth.value)
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
  delModal.value.visible = false
}
</script>

<template>
  <CTableRow class="text-center">
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
      {{ cutString(cash.content, 15) }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(cash.trader, 8) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(cash.bank_account_desc, 10) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="primary">
      {{ numFormat(cash.income || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(cash.outlay || 0) }}
    </CTableDataCell>
    <CTableDataCell>{{ cash.evidence_desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      입출금 거래 건별 수정
    </template>
    <template #default>
      <CashForm
        :cash="cash"
        @multi-submit="multiSubmit"
        @on-delete="deleteConfirm"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>

  <ConfirmModal ref="delModal">
    <template #header>
      <CIcon name="cilWarning" />
      입출금 거래 정보 삭제
    </template>
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
