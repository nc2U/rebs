<template>
  <CModal
    :visible="visible"
    scrollable
    @close="
      () => {
        visible = false
      }
    "
  >
    <CModalHeader>
      <CModalTitle>할일 목록</CModalTitle>
    </CModalHeader>
    <CModalBody>
      <TodoListApp />
    </CModalBody>
  </CModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import TodoListApp from '@/views/_Dashboard/components/TodoListApp/index.vue'

export default defineComponent({
  name: 'TodoModal',
  components: { TodoListApp },
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
