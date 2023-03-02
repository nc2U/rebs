<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount, inject } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const typeSort = inject('typeSort')
const props = defineProps({ type: { type: Object, default: null } })
const emit = defineEmits(['on-update', 'on-delete'])

const form = reactive({
  sort: '',
  name: '',
  color: '',
  actual_area: null,
  supply_area: null,
  contract_area: null,
  average_price: null,
  num_unit: null,
})

const alertModal = ref()
const confirmModal = ref()

const formsCheck = computed(() => {
  if (props.type) {
    const a = form.sort === props.type.sort
    const b = form.name === props.type.name
    const c = form.color === props.type.color
    const d = form.actual_area === props.type.actual_area
    const e = form.supply_area === props.type.supply_area
    const f = form.contract_area === props.type.contract_area
    const g = form.average_price === props.type.average_price
    const h = form.num_unit === props.type.num_unit
    return a && b && c && d && e && f && g && h
  } else return false
})

const formCheck = (bool: boolean) => {
  if (bool) onUpdateType()
  return
}
const onUpdateType = () => {
  if (write_project.value) {
    const pk = props.type.pk
    emit('on-update', { ...{ pk }, ...form })
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}
const onDeleteType = () => {
  if (useAccount().superAuth) confirmModal.value.callModal()
  else {
    alertModal.value.callModal()
    resetForm()
  }
}
const modalAction = () => {
  emit('on-delete', props.type.pk)
  confirmModal.value.visible = false
}
const resetForm = () => {
  form.sort = props.type.sort
  form.name = props.type.name
  form.color = props.type.color
  form.actual_area = props.type.actual_area
  form.supply_area = props.type.supply_area
  form.contract_area = props.type.contract_area
  form.average_price = props.type.average_price
  form.num_unit = props.type.num_unit
}

onBeforeMount(() => {
  if (props.type) resetForm()
})
</script>

<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect
        v-model="form.sort"
        required
        @change="formCheck(form.sort !== type.sort)"
      >
        <option v-for="tp in typeSort" :key="tp.value" :value="tp.value">
          {{ tp.label }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.name"
        maxlength="10"
        placeholder="타입명칭"
        required
        @keypress.enter="formCheck(form.name !== type.name)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.color" title="타입색상" type="color" required />
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model.number="form.actual_area"
        placeholder="전용면적"
        type="number"
        min="0"
        step="0.0001"
        @keypress.enter="formCheck(form.actual_area !== type.actual_area)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.supply_area"
        placeholder="공급면적"
        type="number"
        min="0"
        step="0.0001"
        @keypress.enter="formCheck(form.supply_area !== type.supply_area)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.contract_area"
        placeholder="계약면적"
        type="number"
        min="0"
        step="0.0001"
        @keypress.enter="formCheck(form.contract_area !== type.contract_area)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model.number="form.average_price"
        placeholder="평균가격"
        type="number"
        min="0"
        @keypress.enter="formCheck(form.average_price !== type.average_price)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.num_unit"
        placeholder="세대수"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.num_unit !== type.num_unit)"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        :disabled="formsCheck"
        @click="onUpdateType"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteType">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header> 타입 정보 삭제</template>
    <template #default>
      이 타입에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후 삭제가능
      합니다. 해당 타입을 삭제 하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
