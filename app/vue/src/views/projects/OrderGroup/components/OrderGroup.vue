<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({ order: { type: Object, default: null } })
const emit = defineEmits(['on-update', 'on-delete'])

const form = reactive({
  order_number: null,
  sort: '',
  order_group_name: '',
})

const alertModal = ref()
const confirmModal = ref()

onBeforeMount(() => {
  if (props.order) resetForm()
})

const formsCheck = computed(() => {
  if (props.order) {
    const a = form.order_number === props.order.order_number
    const b = form.sort === props.order.sort
    const c = form.order_group_name === props.order.order_group_name
    return a && b && c
  } else return false
})

const formCheck = (bool: boolean) => {
  if (bool) onUpdateOrder()
  return
}

const onUpdateOrder = () => {
  if (write_project) {
    const pk = props.order.pk
    emit('on-update', { ...{ pk }, ...form })
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}

const accStore = useAccount()
const onDeleteOrder = () => {
  if (accStore.superAuth) confirmModal.value.callModal()
  else {
    alertModal.value.callModal()
    resetForm()
  }
}

const modalAction = () => {
  emit('on-delete', props.order.pk)
  confirmModal.value.visible = false
}

const resetForm = () => {
  form.order_number = props.order.order_number
  form.sort = props.order.sort
  form.order_group_name = props.order.order_group_name
}
</script>

<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.order_number"
        type="number"
        min="1"
        required
        placeholder="등록차수"
        @keypress.enter="formCheck(form.order_number !== order.order_number)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.sort">
        <option value="">구분선택</option>
        <option value="1">일반분양</option>
        <option value="2">조합모집</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.order_group_name"
        maxlength="20"
        placeholder="차수그룹명"
        @keypress.enter="
          formCheck(form.order_group_name !== order.order_group_name)
        "
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        :disabled="formsCheck"
        @click="onUpdateOrder"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteOrder">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-warning" />
      차수그룹 삭제
    </template>
    <template #default>
      이 그룹에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후 삭제가능
      합니다. 해당 차수그룹을 삭제 하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
