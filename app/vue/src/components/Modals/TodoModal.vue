<script lang="ts" setup>
import { ref } from 'vue'
import TodoListApp from '@/components/TodoListApp/index.vue'

const visible = ref(false)

const callModal = () => (visible.value = true)
const close = () => (visible.value = false)
defineExpose({ callModal, close })
</script>

<template>
  <CModal
    :visible="visible"
    scrollable
    @close="() => (visible = false)"
    @keydown.esc="() => (visible = false)"
  >
    <CModalHeader>
      <CModalTitle class="text-body">
        <CIcon name="cilCalendarCheck" class="mr-2" />
        할 일 목록
      </CModalTitle>
    </CModalHeader>
    <CModalBody>
      <TodoListApp />
    </CModalBody>
  </CModal>
</template>
