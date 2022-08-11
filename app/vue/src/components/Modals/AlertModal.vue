<template>
  <CModal
    alignment="center"
    :visible="visible"
    @close="() => (visible = false)"
    @keydown.esc="() => (visible = false)"
  >
    <CModalHeader>
      <CModalTitle>
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

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ConfirmModal',
  data() {
    return {
      headMessage: '',
      bodyMessage: '',
      visible: false,
    }
  },
  methods: {
    callModal(this: any, head?: string, body?: string) {
      if (head) this.headMessage = head
      if (body) this.bodyMessage = body
      this.visible = true
    },
  },
})
</script>
