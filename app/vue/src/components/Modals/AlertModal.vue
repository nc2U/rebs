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
    <CModalHeader class="text-body">
      <CModalTitle>
        <slot name="icon">
          <v-icon
            icon="mdi mdi-alert-circle"
            color="indigo-lighten-2"
            class="mr-2"
          />
        </slot>
        <slot name="header"> {{ headMessage || ' 알림' }}</slot>
      </CModalTitle>
    </CModalHeader>
    <CModalBody class="text-body">
      <slot>
        {{
          bodyMessage ||
          '이 페이지에 대한 등록 및 수정 또는 삭제 권한이 없습니다. \n관리자에게 문의하여 주십시요.'
        }}
      </slot>
    </CModalBody>
    <CModalFooter>
      <CButton color="light" @click="() => (visible = false)"> 닫기</CButton>
    </CModalFooter>
  </CModal>
</template>
