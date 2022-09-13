<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount } from 'vue'
import { useAccount } from '@/store/pinia/account'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { write_project } from '@/utils/pageAuth'

const props = defineProps({ floor: { type: Object, default: null } })
const emit = defineEmits(['on-update', 'on-delete'])

const alertModal = ref()
const confirmModal = ref()

const form = reactive({
  start_floor: null,
  end_floor: null,
  extra_cond: '',
  alias_name: '',
})

onBeforeMount(() => {
  if (props.floor) resetForm()
})

const formsCheck = computed(() => {
  if (props.floor) {
    const a = form.start_floor === props.floor.start_floor
    const b = form.end_floor === props.floor.end_floor
    const c = form.extra_cond === props.floor.extra_cond
    const d = form.alias_name === props.floor.alias_name
    return a && b && c && d
  } else return false
})

const formCheck = (bool: boolean) => {
  if (bool) onUpdateFloor()
  return
}

const onUpdateFloor = () => {
  if (write_project) {
    const pk = props.floor.pk
    emit('on-update', { ...{ pk }, ...form })
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}

const onDeleteFloor = () => {
  if (useAccount().superAuth) confirmModal.value.callModal()
  else {
    alertModal.value.callModal()
    resetForm()
  }
}
const modalAction = () => {
  emit('on-delete', props.floor.pk)
  confirmModal.value.visible = false
}
const resetForm = () => {
  form.start_floor = props.floor.start_floor
  form.end_floor = props.floor.end_floor
  form.extra_cond = props.floor.extra_cond
  form.alias_name = props.floor.alias_name
}
</script>

<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.start_floor"
        placeholder="시작 층"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.start_floor !== floor.start_floor)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.end_floor"
        placeholder="종료 층"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.end_floor !== form.end_floor)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model="form.extra_cond"
        maxlength="20"
        placeholder="방향/위치"
        @keypress.enter="formCheck(form.extra_cond !== floor.extra_cond)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model="form.alias_name"
        maxlength="20"
        placeholder="층별 범위 명칭"
        required
        @keypress.enter="formCheck(form.alias_name !== floor.alias_name)"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        :disabled="formsCheck"
        @click="onUpdateFloor"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteFloor">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-warning" />
      층별 타입 삭제
    </template>
    <template #default>
      이 타입에 종속된 분양가 데이터가 있는 경우 해당 데이터를 모두 제거한 후
      삭제가능 합니다. 해당 층별 타입을 삭제 하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
