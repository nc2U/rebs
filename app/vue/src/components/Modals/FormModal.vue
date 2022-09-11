<script lang="ts" setup>
import { ref } from 'vue'

const visible = ref(false)

const callModal = () => (visible.value = true)
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
        <slot name="header">Title</slot>
      </CModalTitle>
    </CModalHeader>
    <slot>
      <CModalBody> Form here...</CModalBody>
      <CModalFooter>
        <CButton color="light" @click="() => (visible = false)"> 닫기</CButton>
        <CButton color="primary">Save changes</CButton>
      </CModalFooter>
    </slot>
  </CModal>
</template>
