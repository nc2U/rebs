<template>
  <section class="todoapp mb-4">
    <!-- header -->
    <header class="header">
      <input
        class="new-todo"
        autofocus
        autocomplete="off"
        placeholder="나의 할일 목록 관리"
        @keyup.enter="addTodo"
      />
    </header>
    <!-- main section -->
    <section v-show="todos.length" class="main">
      <input
        id="toggle-all"
        :checked="allChecked"
        class="toggle-all"
        type="checkbox"
        @change="toggleAll({ done: !allChecked })"
      />
      <label for="toggle-all" />
      <ul class="todo-list">
        <Todo
          v-for="(todo, index) in filteredTodos"
          :key="index"
          :todo="todo"
          @toggleTodo="toggleTodo"
          @editTodo="editTodo"
          @deleteTodo="deleteTodo"
        />
      </ul>
    </section>
    <!-- footer -->
    <footer v-show="todos.length" class="footer">
      <span class="todo-count">
        <strong>{{ remaining }}</strong>
        {{ remaining }} left
      </span>
      <ul class="filters">
        <li v-for="(val, key) in filters" :key="key">
          <a
            :class="{ selected: visibility === key }"
            @click.prevent="visibility = key"
          >
            {{ key }}
          </a>
        </li>
      </ul>

      <button
        class="clear-completed"
        v-show="todos.length > remaining"
        @click="clearCompleted"
      >
        Clear completed
      </button>
    </footer>
  </section>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Todo from './Todo.vue'

interface todo {
  title: string
  done: boolean
}

const STORAGE_KEY = 'todos'
const filters = {
  all: (todos: todo[]) => todos,
  active: (todos: todo[]) => todos.filter((todo) => !todo.done),
  completed: (todos: todo[]) => todos.filter((todo) => todo.done),
}
const defalutList = [
  { text: 'star this repository', done: false },
  { text: 'fork this repository', done: false },
  { text: 'follow author', done: false },
  { text: 'vue-element-admin', done: true },
  { text: 'vue', done: true },
  { text: 'element-ui', done: true },
  { text: 'axios', done: true },
  { text: 'webpack', done: true },
]
export default defineComponent({
  name: 'TodoListApp',
  components: { Todo },
  // filters: {
  //   pluralize: (n: any, w: any) => (n === 1 ? w : w + 's'),
  //   capitalize: (s: any) => s.charAt(0).toUpperCase() + s.slice(1),
  // },
  data() {
    return {
      visibility: 'all',
      filters,
      todos:
        JSON.parse((window as any).localStorage.getItem(STORAGE_KEY)) ||
        defalutList,
      // todos: defalutList,
    }
  },
  computed: {
    allChecked() {
      return (this as any).todos.every((todo: todo) => todo.done)
    },
    filteredTodos() {
      return filters[this.visibility](this.todos) as todo[]
    },
    remaining() {
      return (this as any).todos.filter((todo: todo) => !todo.done).length
    },
  },
  methods: {
    setLocalStorage() {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(this.todos))
    },
    addTodo(e: any) {
      const text = e.target.value
      if (text.trim()) {
        this.todos.push({
          text,
          done: false,
        })
        this.setLocalStorage()
      }
      e.target.value = ''
    },
    toggleTodo(val: any) {
      val.done = !val.done
      this.setLocalStorage()
    },
    deleteTodo(todo: any) {
      this.todos.splice(this.todos.indexOf(todo), 1)
      this.setLocalStorage()
    },
    editTodo({ todo, value }: any) {
      todo.text = value
      this.setLocalStorage()
    },
    clearCompleted() {
      this.todos = this.todos.filter((todo) => !todo.done)
      this.setLocalStorage()
    },
    toggleAll({ done }: any) {
      this.todos.forEach((todo) => {
        todo.done = done
        this.setLocalStorage()
      })
    },
  },
})
</script>

<style lang="scss">
@import './index.scss';
</style>
