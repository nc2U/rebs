<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount, inject } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const d1List = inject('d1List')
const d2List = inject('d2List')

const props = defineProps({ budget: { type: Object, default: null } })
const emit = defineEmits(['on-update', 'on-delete'])

const form = reactive({
  pk: null,
  account_d1: null,
  account_d2: null,
  item_name: '',
  basis_calc: null,
  budget: null,
})

const alertModal = ref()
const confirmModal = ref()

onBeforeMount(() => {
  if (props.budget) resetForm()
})

const formsCheck = computed(() => {
  if (props.budget) {
    const a = form.pk === props.budget.pk
    const b = form.account_d1 === props.budget.account_d1
    const c = form.account_d2 === props.budget.account_d2
    const d = form.item_name === props.budget.item_name
    const e = form.basis_calc === props.budget.basis_calc
    const f = form.budget === props.budget.budget
    return a && b && c && d && e && f
  } else return false
})

const formCheck = (bool: boolean) => {
  if (bool) onUpdateBudget()
  return
}

const onUpdateBudget = () => {
  if (write_project.value) {
    emit('on-update', { ...form })
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}

const accStore = useAccount()
const onDeleteBudget = () => {
  if (accStore.superAuth) confirmModal.value.callModal()
  else {
    alertModal.value.callModal()
    resetForm()
  }
}

const modalAction = () => {
  emit('on-delete', props.budget.pk)
  confirmModal.value.close()
}

const resetForm = () => {
  form.pk = props.budget.pk
  form.account_d1 = props.budget.account_d1
  form.account_d2 = props.budget.account_d2
  form.item_name = props.budget.item_name
  form.basis_calc = props.budget.basis_calc
  form.budget = props.budget.budget
}
</script>

<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect v-model="form.account_d1" required>
        <option value="">대분류</option>
        <option v-for="d1 in d1List" :key="d1.pk" :value="d1.pk">
          {{ d1.name }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.account_d2" required>
        <option value="">중분류</option>
        <option v-for="d2 in d2List" :key="d2.pk" :value="d2.pk">
          {{ d2.name }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.item_name" placeholder="항목명" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.basis_calc" placeholder="산출 근거" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.budget"
        type="number"
        min="0"
        placeholder="지출 예산"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        :disabled="formsCheck"
        @click="onUpdateBudget"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteBudget">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header> 지출 예산 삭제</template>
    <template #default> 해당 지출 예산 항목을 삭제 하시겠습니까?</template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
