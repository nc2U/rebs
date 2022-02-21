<template>
  <CModal
    alignment="center"
    :visible="visible"
    @close="() => (visible = false)"
  >
    <CModalHeader>
      <CModalTitle>
        <CIcon name="cilItalic" />
        <slot name="header"> 알림</slot>
      </CModalTitle>
    </CModalHeader>
    <CModalBody>
      <slot>
        이 페이지에 대한 등록 및 수정 또는 삭제 권한이 없습니다. 담당자에게
        문의하여 주십시요.
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
      visible: false,
    }
  },
  methods: {
    callModal() {
      this.visible = true
    },
  },
})
</script>
