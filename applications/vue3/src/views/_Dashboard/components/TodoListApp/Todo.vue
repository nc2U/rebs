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
      v-focus="editing"
      :value="todo.title"
      class="edit"
      @keyup.enter="doneEdit"
      @keyup.esc="cancelEdit"
      @blur="doneEdit"
    />
  </li>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Todo',
  directives: {
    focus(el, { value }) {
      if (value) {
        el.focus()
      }
    },
  },
  props: {
    todo: {
      type: Object,
      default: function () {
        return {}
      },
    },
  },
  data() {
    return {
      editing: false,
    }
  },
  methods: {
    delTodo(todo: any) {
      this.$emit('delTodo', todo)
    },
    editTodo({ todo, title }: any) {
      this.$emit('editTodo', { todo, title })
    },
    toggleTodo(todo: any) {
      this.$emit('toggleTodo', todo)
    },
    doneEdit(e: any) {
      const title = e.target.value.trim()
      const { todo }: any = this
      if (!title) {
        // console.log(todo)
        this.delTodo(todo)
      } else if (this.editing) {
        this.editTodo({
          todo,
          title,
        })
      }
      this.editing = false
    },
    cancelEdit(e: any) {
      e.target.value = (this as any).todo.title
      this.editing = false
    },
  },
})
</script>
