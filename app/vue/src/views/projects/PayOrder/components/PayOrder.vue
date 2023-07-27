<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { write_project } from '@/utils/pageAuth'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const emit = defineEmits(['on-update', 'on-delete'])
const props = defineProps({ payOrder: { type: Object, required: true } })

const form = reactive({
  pay_sort: '',
  pay_code: null as string | null,
  pay_time: null as string | null,
  pay_name: '',
  alias_name: '',
  is_pm_cost: false,
  pay_due_date: null as string | null,
  extra_due_date: null as string | null,
})

const refAlertModal = ref()
const refConfirmModal = ref()

const formsCheck = computed(() => {
  const a = form.pay_sort === props.payOrder.pay_sort
  const b = form.pay_code === props.payOrder.pay_code
  const c = form.pay_time === props.payOrder.pay_time
  const d = form.pay_name === props.payOrder.pay_name
  const e = form.alias_name === props.payOrder.alias_name
  const f = form.is_pm_cost === props.payOrder.is_pm_cost
  const g = form.pay_due_date === props.payOrder.pay_due_date
  const h = form.extra_due_date === props.payOrder.extra_due_date
  return a && b && c && d && e && f && g && h
})

const formCheck = (bool: boolean) => {
  if (bool) onUpdatePayOrder()
  return
}
const onUpdatePayOrder = () => {
  if (write_project.value) {
    const pk = props.payOrder.pk
    emit('on-update', { ...{ pk }, ...form })
  } else {
    refAlertModal.value.callModal()
    dataSetup()
  }
}
const onDeletePayOrder = () => {
  if (useAccount().superAuth) refConfirmModal.value.callModal()
  else {
    refAlertModal.value.callModal()
    dataSetup()
  }
}
const modalAction = () => {
  emit('on-delete', props.payOrder.pk)
  refConfirmModal.value.close()
}

const dataSetup = () => {
  form.pay_sort = props.payOrder.pay_sort
  form.pay_code = props.payOrder.pay_code
  form.pay_time = props.payOrder.pay_time
  form.pay_name = props.payOrder.pay_name
  form.alias_name = props.payOrder.alias_name
  form.is_pm_cost = props.payOrder.is_pm_cost
  form.pay_due_date = props.payOrder.pay_due_date
  form.extra_due_date = props.payOrder.extra_due_date
}

onBeforeMount(() => dataSetup())
</script>

<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect v-model="form.pay_sort" required>
        <option value="">종류선택</option>
        <option value="1">계약금</option>
        <option value="2">중도금</option>
        <option value="3">잔금</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.pay_code"
        placeholder="납입회차 코드"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.pay_code !== payOrder.pay_code)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.pay_time"
        placeholder="납부순서"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.pay_time !== payOrder.pay_time)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <CCol class="pt-2 pl-3">
        <CFormSwitch
          v-model="form.is_pm_cost"
          :checked="payOrder.is_pm_cost === true"
        />
      </CCol>
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model="form.pay_name"
        maxlength="20"
        placeholder="납부회차 명"
        required
        @keypress.enter="formCheck(form.pay_name !== payOrder.pay_name)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model="form.alias_name"
        maxlength="20"
        placeholder="회차 별칭"
        required
        @keypress.enter="formCheck(form.alias_name !== payOrder.alias_name)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <DatePicker
        v-model="form.pay_due_date"
        maxlength="10"
        placeholder="납부기한일"
        :required="false"
        @keypress.enter="formCheck(form.pay_due_date !== payOrder.pay_due_date)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <DatePicker
        v-model="form.extra_due_date"
        maxlength="10"
        placeholder="납부유예일"
        :required="false"
        @keypress.enter="
          formCheck(form.extra_due_date !== payOrder.extra_due_date)
        "
      />
    </CTableDataCell>

    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        :disabled="formsCheck"
        @click="onUpdatePayOrder"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeletePayOrder">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="refConfirmModal">
    <template #header> 납부 회차 삭제</template>
    <template #default>
      프로젝트 입출금 데이터에 이 납부 회차 정보가 등록되어 있는 경우 해당
      데이터에서 납부 회차 정보가 삭제됩니다. 이 납부 회차 정보를 삭제
      하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="refAlertModal" />
</template>
