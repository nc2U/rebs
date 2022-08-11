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
    <slot>
      <CModalBody> Form here...</CModalBody>
      <CModalFooter>
        <CButton color="light" @click="() => (visible = false)"> 닫기</CButton>
        <CButton color="primary">Save changes</CButton>
      </CModalFooter>
    </slot>
  </CModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'FormModal',
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
