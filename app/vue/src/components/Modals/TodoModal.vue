<template>
  <CModal
    :visible="visible"
    scrollable
    @close="() => (visible = false)"
    @keydown.esc="() => (visible = false)"
  >
    <CModalHeader>
      <CModalTitle>
        <CIcon name="cilCalendarCheck" class="mr-2" />
        할 일 목록
      </CModalTitle>
    </CModalHeader>
    <CModalBody>
      <TodoListApp />
    </CModalBody>
  </CModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import TodoListApp from '@/components/TodoListApp/index.vue'

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
