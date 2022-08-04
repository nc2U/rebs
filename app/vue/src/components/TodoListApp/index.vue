<template>
  <section class="todoapp mb-4">
    <!-- header -->
    <header class="header">
      <input
        class="new-todo"
        autofocus
        autocomplete="off"
        placeholder="해야 할 일이 있나요?"
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
        @change="toggleAll({ completed: !allChecked })"
      />
      <label for="toggle-all" />
      <ul class="todo-list">
        <Todo
          v-for="(todo, index) in filteredTodos"
          :key="index"
          :todo="todo"
          @toggleTodo="toggleTodo"
          @editTodo="editTodo"
          @delTodo="delTodo"
        />
      </ul>
    </section>
    <!-- footer -->
    <footer v-show="todos.length" class="footer">
      <span class="todo-count">
        <strong>{{ remaining }}</strong> {{ pluralize(remaining, 'item') }} left
      </span>
      <ul class="filters">
        <li v-for="(val, key) in filters" :key="key">
          <a
            :class="{ selected: visibility === key }"
            @click.prevent="visibility = key"
          >
            {{ capitalize(key) }}
          </a>
        </li>
      </ul>

      <button
        v-show="todos.length > remaining"
        class="clear-completed"
        @click="clearCompleted"
      >
        Clear completed
      </button>
    </footer>
  </section>

  <footer class="info text-center" style="color: #ccc; font-size: 0.875rem">
    <p v-if="todos.length" class="aa">
      할 일 목록을 수정하려면 더블클릭 하세요.
    </p>
    <p v-else class="aa">첫 번째 할 일 목록을 메모해 보세요.</p>
  </footer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Todo from './Todo.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

interface todo {
  id: number
  title: string
  completed: boolean
  soft_deleted: boolean
}

type filterType = {
  [index: string]: (x: todo[]) => ((y: todo) => boolean) | todo[]
}

const filters: filterType = {
  all: (todos: todo[]) => todos,
  active: (todos: todo[]) => todos.filter(todo => !todo.completed),
  completed: (todos: todo[]) => todos.filter(todo => todo.completed),
}
const defalutList = [
  {
    id: 500,
    title: 'star this repository',
    completed: false,
    soft_deleted: false,
  },
  {
    id: 501,
    title: 'fork this repository',
    completed: false,
    soft_deleted: false,
  },
  { id: 502, title: 'follow author', completed: false, soft_deleted: false },
  { id: 503, title: 'vue-element-admin', completed: true, soft_deleted: false },
  { id: 504, title: 'vue', completed: true, soft_deleted: false },
  { id: 505, title: 'element-ui', completed: true, soft_deleted: false },
  { id: 506, title: 'axios', completed: true, soft_deleted: false },
  { id: 507, title: 'webpack', completed: true, soft_deleted: false },
]
export default defineComponent({
  name: 'TodoListApp',
  components: { Todo },
  data() {
    return {
      visibility: 'all',
      filters,
    }
  },
  created() {
    this.fetchTodoList()
  },
  computed: {
    todos() {
      return (this as any).myTodos
    },
    allChecked() {
      return (this as any).todos.every((todo: todo) => todo.completed)
    },
    filteredTodos() {
      return filters[(this as any).visibility]((this as any).todos)
    },
    remaining() {
      return (this as any).todos.filter((todo: todo) => !todo.completed).length
    },
    ...mapState('accounts', ['userInfo']),
    ...mapGetters('accounts', ['myTodos']),
  },
  methods: {
    addTodo(e: any) {
      const title = e.target.value
      if (title.trim()) {
        this.createTodo({ user: this.userInfo.pk, title })
      }
      e.target.value = ''
    },
    toggleTodo(todo: any) {
      todo.completed = !todo.completed
      const payload = { pk: todo.pk, completed: todo.completed }
      this.patchTodo(payload)
    },
    delTodo(todo: any) {
      const { pk } = todo
      const soft_deleted = true
      const payload = { pk, soft_deleted }
      this.patchTodo(payload)
    },
    editTodo({ todo, title }: any) {
      const { pk } = todo
      const payload = { pk, title }
      this.patchTodo(payload)
    },
    clearCompleted() {
      this.todos.forEach((todo: any) => {
        if (todo.completed === true) {
          const payload = { pk: todo.pk, soft_deleted: true }
          this.patchTodo(payload)
        }
      })
    },
    toggleAll({ completed }: any) {
      this.todos.forEach((todo: any) => {
        todo.completed = completed
        const payload = { pk: todo.pk, completed: todo.completed }
        this.patchTodo(payload)
      })
    },
    pluralize: (n: any, w: any) => (n === 1 ? w : w + 's'),
    capitalize: (s: any) => s.charAt(0).toUpperCase() + s.slice(1),
    ...mapActions('accounts', ['fetchTodoList', 'createTodo', 'patchTodo']),
  },
})
</script>

<style lang="scss">
@import 'index';
</style>
