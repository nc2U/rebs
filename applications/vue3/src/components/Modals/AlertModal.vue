<template>
  <CModal
    alignment="center"
    :visible="visible"
    @close="
      () => {
        visible = false
      }
    "
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
      <CButton
        color="light"
        @click="
          () => {
            visible = false
          }
        "
      >
        닫기
      </CButton>
      <slot name="footer">
        <CButton color="primary" @click="onAlert">Save changes</CButton>
      </slot>
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
    onAlert() {
      this.$emit('on-confirm')
    },
  },
})
</script>
