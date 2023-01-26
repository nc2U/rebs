<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount } from 'vue'
import { useAccount } from '@/store/pinia/account'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { write_project } from '@/utils/pageAuth'

const props = defineProps({ building: { type: Object, default: null } })
const emit = defineEmits(['on-update', 'on-delete'])

const alertModal = ref()
const confirmModal = ref()

const form = reactive({ name: '' })

const formsCheck = computed(() => form.name === props.building.name)

onBeforeMount(() => {
  if (props.building) resetForm()
})

const formCheck = (bool: boolean) => {
  if (bool) onUpdateBuilding()
  return
}

const onUpdateBuilding = () => {
  if (write_project.value) {
    const pk = props.building.pk
    emit('on-update', { ...{ pk }, ...form })
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}

const onDeleteBuilding = () => {
  if (useAccount().superAuth) confirmModal.value.callModal()
  else {
    alertModal.value.callModal()
    resetForm()
  }
}

const modalAction = () => {
  emit('on-delete', props.building.pk)
  confirmModal.value.close()
}

const resetForm = () => (form.name = props.building.name)
</script>

<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        v-model="form.name"
        maxlength="10"
        placeholder="동(건물)"
        @keypress.enter="formCheck(form.name !== building.name)"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        :disabled="formsCheck"
        @click="onUpdateBuilding"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteBuilding">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header> 동(건물) 삭제 </template>
    <template #default>
      이 동(건물)에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후
      삭제가능 합니다. 해당 동(건물)을 삭제 하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
