<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { numFormat, cutString } from '@/utils/baseMixins'
import { ProBankAcc, ProjectCashBook } from '@/store/types/proCash'
import FormModal from '@/components/Modals/FormModal.vue'
import ProCashForm from '@/views/proCash/Manage/components/ProCashForm.vue'

const props = defineProps({
  proCash: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete', 'on-bank-update'])

const updateFormModal = ref()

const sortClass = computed(
  () => ['', 'text-primary', 'text-danger', 'text-info'][props.proCash.sort],
)

const store = useStore()
const dark = computed(() => store.state.theme === 'dark')
const rowColor = computed(() => {
  let color = ''
  color =
    props.proCash.contract &&
    (props.proCash.project_account_d2 === 1 ||
      props.proCash.project_account_d2 === 4)
      ? 'info'
      : color
  color = dark.value ? '' : color
  color = props.proCash.is_separate ? 'primary' : color
  color = props.proCash.separated ? 'secondary' : color
  return color
})

const showDetail = () => updateFormModal.value.callModal()

const multiSubmit = (payload: {
  formData: ProjectCashBook
  sepData: ProjectCashBook | null
}) => emit('multi-submit', payload)

const onDelete = (payload: { project: number; pk: number }) =>
  emit('on-delete', payload)

const onBankUpdate = (payload: ProBankAcc) => emit('on-bank-update', payload)
</script>

<template>
  <CTableRow
    v-if="proCash"
    class="text-center"
    :color="rowColor"
    :style="proCash.is_separate ? 'font-weight: bold;' : ''"
  >
    <CTableDataCell>{{ proCash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ proCash.sort_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ proCash.project_account_d1_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <span v-if="proCash.project_account_d2_desc">
        {{ cutString(proCash.project_account_d2_desc, 9) }}
      </span>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <span v-if="proCash.content">
        {{ cutString(proCash.content, 10) }}
      </span>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <span v-if="proCash.trader">
        {{ cutString(proCash.trader, 9) }}
      </span>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <span v-if="proCash.bank_account_desc">
        {{ cutString(proCash.bank_account_desc, 9) }}
      </span>
    </CTableDataCell>
    <CTableDataCell class="text-right" :color="dark ? '' : 'success'">
      {{ numFormat(proCash.income || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" :color="dark ? '' : 'danger'">
      {{ numFormat(proCash.outlay || 0) }}
    </CTableDataCell>
    <CTableDataCell>{{ proCash.evidence_desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>프로젝트 입출금 거래 건별 관리</template>
    <template #default>
      <ProCashForm
        :pro-cash="proCash"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
        @onBankUpdate="onBankUpdate"
      />
    </template>
  </FormModal>
</template>
