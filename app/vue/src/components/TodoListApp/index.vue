<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import Todo from './Todo.vue'

interface Todo {
  pk: number
  title: string
  completed: boolean
  soft_deleted: boolean
}

const account = useAccount()

const visibility = ref('all')
const todos = ref<Todo[]>([])

type filterType = {
  [key: string]: (x: Todo[]) => ((y: Todo) => boolean) | Todo[]
}

const userInfo = computed(() => account.userInfo)
const myTodos = computed(() => account.myTodos)
watch(myTodos, val => (todos.value = val))

const filters: filterType = {
  all: (myTodos: Todo[]) => myTodos,
  active: (myTodos: Todo[]) => myTodos.filter(todo => !todo.completed),
  completed: (myTodos: Todo[]) => myTodos.filter(todo => todo.completed),
}

const allChecked = computed(() => myTodos.value.every(todo => todo.completed))

const filteredTodos = computed(() => filters[visibility.value](todos.value))

const remaining = computed(
  () => todos.value.filter((todo: todo) => !todo.completed).length,
)

// ...mapActions('accounts', ['fetchTodoList', 'createTodo', 'patchTodo']),

const addTodo = (e: any) => {
  const title = e.target.value.trim()
  if (userInfo.value && title) {
    account.createTodo({ user: userInfo.value.pk, title })
  }
  e.target.value = ''
}

const toggleTodo = (todo: Todo) => {
  todo.completed = !todo.completed
  const payload = { pk: todo.pk, completed: todo.completed }
  account.patchTodo(payload)
}

const delTodo = (todo: Todo) => {
  const { pk } = todo
  const soft_deleted = true
  const payload = { pk, soft_deleted }
  account.patchTodo(payload)
}

const editTodo = ({ todo, title }: { todo: Todo; title: string }) => {
  const { pk } = todo
  const payload = { pk, title }
  account.patchTodo(payload)
}

const clearCompleted = () => {
  todos.value.forEach((todo: Todo) => {
    if (todo.completed) {
      const payload = { pk: todo.pk, soft_deleted: true }
      account.patchTodo(payload)
    }
  })
}

const toggleAll = ({ completed }: { completed: boolean }) => {
  todos.value.forEach((todo: Todo) => {
    todo.completed = completed
    const payload = { pk: todo.pk, completed: todo.completed }
    account.patchTodo(payload)
  })
}

const pluralize = (n: any, w: any) => (n === 1 ? w : w + 's')
const capitalize = (s: any) => s.charAt(0).toUpperCase() + s.slice(1)

onBeforeMount(() => account.fetchTodoList())
</script>

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

<style lang="scss">
@import 'index';
</style>
