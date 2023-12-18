<script lang="ts" setup>
import { ref } from 'vue'

const visible = ref(false)
const headerMessage = ref('알림')
const bodyMessage = ref('')
const headIcon = ref('mdi-arrow-right-bold-box')
const headerColor = ref('indigo-lighten-2')

const callModal = (head?: string, body?: string, icon?: string, color = 'indigo-lighten-2') => {
  if (head) headerMessage.value = head
  if (body) bodyMessage.value = body
  if (icon) headIcon.value = icon
  if (color) headerColor.value = color
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
          <v-icon :icon="headIcon" :color="headerColor" class="mr-2" />
        </slot>
        <slot name="header">{{ headerMessage }}</slot>
      </CModalTitle>
    </CModalHeader>
    <CModalBody class="text-body" style="line-height: 26px">
      <slot>
        {{
          bodyMessage ||
          'Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in,\n' +
            'egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.'
        }}
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
