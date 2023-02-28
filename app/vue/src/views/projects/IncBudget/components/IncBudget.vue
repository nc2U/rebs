<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount, inject } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const d1List = inject('d1List')
const d2List = inject('d2List')
const orderGroups = inject('orderGroups')
const unitTypes = inject('unitTypes')

const props = defineProps({ budget: { type: Object, default: null } })
const emit = defineEmits(['on-update', 'on-delete'])

const form = reactive({
  pk: null,
  account_d1: null,
  account_d2: null,
  order_group: null,
  unit_type: null,
  item_name: '',
  average_price: null,
  quantity: null,
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
    const d = form.order_group === props.budget.order_group
    const e = form.unit_type === props.budget.unit_type
    const f = form.item_name === props.budget.item_name
    const g = form.average_price === props.budget.average_price
    const h = form.quantity === props.budget.quantity
    const i = form.budget === props.budget.budget
    return a && b && c && d && e && f && g && h && i
  } else return false
})

const formCheck = (bool: boolean) => {
  if (bool) onUpdateBudget()
  return
}

const onUpdateBudget = () => {
  if (write_project.value) {
    const pk = props.budget.pk
    emit('on-update', { ...{ pk }, ...form })
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
  form.order_group = props.budget.order_group
  form.unit_type = props.budget.unit_type
  form.item_name = props.budget.item_name
  form.average_price = props.budget.average_price
  form.quantity = props.budget.quantity
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
      <CFormSelect v-model="form.order_group">
        <option value="">차수</option>
        <option v-for="og in orderGroups" :key="og.value" :value="og.value">
          {{ og.label }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.unit_type">
        <option value="">타입</option>
        <option v-for="ut in unitTypes" :key="ut.value" :value="ut.value">
          {{ ut.label }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.item_name" placeholder="항목명칭" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.average_price"
        type="number"
        min="0"
        placeholder="평균가격"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.quantity"
        type="number"
        min="0"
        placeholder="수량"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.budget"
        type="number"
        min="0"
        placeholder="수입예산"
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
    <template #header> 수입 예산 삭제</template>
    <template #default> 해당 수입 예산 항목을 삭제 하시겠습니까?</template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
