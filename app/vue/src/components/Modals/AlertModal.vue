<script lang="ts" setup>
import { ref } from 'vue'

const headMessage = ref('')
const bodyMessage = ref('')
const visible = ref(false)
const callModal = (head?: string, body?: string) => {
  if (head) headMessage.value = head
  if (body) bodyMessage.value = body
  visible.value = true
}
const close = () => (visible.value = false)
defineExpose({ callModal, close })
</script>

<template>
  <CModal
    alignment="center"
    :visible="visible"
    @close="() => (visible = false)"
    @keydown.esc="() => (visible = false)"
  >
    <CModalHeader>
      <CModalTitle class="text-body">
        <CIcon name="cilItalic" />
        <slot name="header"> {{ headMessage || ' 알림' }}</slot>
      </CModalTitle>
    </CModalHeader>
    <CModalBody>
      <slot>
        {{
          bodyMessage ||
          '이 페이지에 대한 등록 및 수정 또는 삭제 권한이 없습니다. 관리자에게 문의하여 주십시요.'
        }}
      </slot>
    </CModalBody>
    <CModalFooter>
      <CButton color="light" @click="() => (visible = false)"> 닫기</CButton>
    </CModalFooter>
  </CModal>
</template>
