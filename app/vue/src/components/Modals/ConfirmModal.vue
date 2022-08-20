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
      <CModalTitle>
        <slot name="header">Title</slot>
      </CModalTitle>
    </CModalHeader>
    <CModalBody>
      <slot>
        Cras mattis consectetur purus sit amet fermentum. Cras justo odio,
        dapibus ac facilisis in, egestas eget quam. Morbi leo risus, porta ac
        consectetur ac, vestibulum at eros.
      </slot>
    </CModalBody>
    <CModalFooter>
      <CButton color="light" @click="() => (visible = false)"> 닫기</CButton>
      <slot name="footer">
        <CButton color="primary">Save changes</CButton>
      </slot>
    </CModalFooter>
  </CModal>
</template>
