<template>
  <li :class="{ completed: todo.completed, editing: editing }" class="todo">
    <div class="view">
      <input
        :checked="todo.completed"
        class="toggle"
        type="checkbox"
        @change="toggleTodo(todo)"
      />
      <label @dblclick="editing = true" v-text="todo.title" />
      <button class="destroy" @click="delTodo(todo)" />
    </div>
    <input
      v-show="editing"
      ref="editInput"
      :value="todo.title"
      class="edit"
      @keyup.enter="doneEdit"
      @keyup.esc="cancelEdit"
      @blur="doneEdit"
    />
  </li>
</template>

<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { Todo } from '@/store/types/accounts'

const props = defineProps({ todo: { type: Object, default: null } })

const emit = defineEmits(['delTodo', 'editTodo', 'toggleTodo'])

const editInput = ref()
const editing = ref(false)

watch(editing, val => {
  if (val) nextTick(() => editInput.value.focus())
})

const delTodo = (pk: number) => emit('delTodo', pk)

const editTodo = (pk: number, title: string) => {
  if (props.todo.title !== title) emit('editTodo', pk, title)
  else return
}

const toggleTodo = (todo: Todo) => emit('toggleTodo', todo)

const doneEdit = (e: Event) => {
  const title = (e.target as HTMLInputElement).value.trim()
  if (!title) delTodo(props.todo.pk)
  else if (editing.value) editTodo(props.todo.pk, title)
  editing.value = false
}
const cancelEdit = (e: Event) => {
  ;(e.target as HTMLInputElement).value = props.todo.title
  editing.value = false
}
</script>
