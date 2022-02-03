<template>
  <section class="todoapp">
    <header class="header">
      <!--      <h1>todos</h1>-->
      <input
        class="new-todo"
        autofocus
        autocomplete="off"
        placeholder="Todo List - What needs to be done?"
        v-model="newTodo"
        @keyup.enter="addTodo"
      />
    </header>
    <section class="main" v-show="todos.length" v-cloak>
      <input
        id="toggle-all"
        class="toggle-all"
        type="checkbox"
        v-model="allDone"
      />
      <label for="toggle-all"></label>
      <ul class="todo-list">
        <li
          v-for="todo in filteredTodos"
          class="todo"
          :key="todo.id"
          :class="{ completed: todo.completed, editing: todo == editedTodo }"
        >
          <div class="view">
            <input class="toggle" type="checkbox" v-model="todo.completed" />
            <label @dblclick="editTodo(todo)">{{ todo.title }}</label>
            <button class="destroy" @click="removeTodo(todo)"></button>
          </div>
          <input
            class="edit"
            type="text"
            v-model="todo.title"
            v-todo-focus="todo == editedTodo"
            @blur="doneEdit(todo)"
            @keyup.enter="doneEdit(todo)"
            @keyup.esc="cancelEdit(todo)"
          />
        </li>
      </ul>
    </section>
    <footer class="footer" v-show="todos.length" v-cloak>
      <span class="todo-count">
        <strong>{{ remaining }}</strong> {{ remaining | pluralize }} left
      </span>
      <ul class="filters">
        <li>
          <a href="#/all" :class="{ selected: visibility == 'all' }">All</a>
        </li>
        <li>
          <a href="#/active" :class="{ selected: visibility == 'active' }"
            >Active</a
          >
        </li>
        <li>
          <a href="#/completed" :class="{ selected: visibility == 'completed' }"
            >Completed</a
          >
        </li>
      </ul>
      <button
        class="clear-completed"
        @click="removeCompleted"
        v-show="todos.length > remaining"
      >
        Clear completed
      </button>
    </footer>
  </section>
  <!--  <footer class="info">-->
  <!--    <p>Double-click to edit a todo</p>-->
  <!--    <p>Written by <a href="http://evanyou.me">Evan You</a></p>-->
  <!--    <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>-->
  <!--  </footer>-->
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: '',
  // app initial state
  data() {
    return {
      todos: [],
      newTodo: '',
      editedTodo: null,
      visibility: 'all',
    }
  },
  computed: {
    // filteredTodos() {
    //   return filters[this.visibility](this.todos)
    // },
    // remaining() {
    //   return filters.active(this.todos).length
    // },
    // allDone: {
    //   get() {
    //     return this.remaining === 0
    //   },
    //   set(value) {
    //     this.todos.forEach((todo) => {
    //       todo.completed = value
    //     })
    //   },
    // },
  },
  methods: {
    // pluralize(n) {
    //   return n === 1 ? 'item' : 'items'
    // },
    // addTodo() {
    //   var value = this.newTodo && this.newTodo.trim()
    //   if (!value) {
    //     return
    //   }
    //   this.todos.push({
    //     id: todoStorage.uid++,
    //     title: value,
    //     completed: false,
    //   })
    //   this.newTodo = ''
    // },
    //
    // removeTodo(todo) {
    //   this.todos.splice(this.todos.indexOf(todo), 1)
    // },
    //
    // editTodo(todo) {
    //   this.beforeEditCache = todo.title
    //   this.editedTodo = todo
    // },
    //
    // doneEdit(todo) {
    //   if (!this.editedTodo) {
    //     return
    //   }
    //   this.editedTodo = null
    //   todo.title = todo.title.trim()
    //   if (!todo.title) {
    //     this.removeTodo(todo)
    //   }
    // },
    //
    // cancelEdit(todo) {
    //   this.editedTodo = null
    //   todo.title = this.beforeEditCache
    // },
    //
    // removeCompleted() {
    //   this.todos = filters.active(this.todos)
    // },
  },
  directives: {
    'todo-focus': {
      updated(el, binding) {
        if (binding.value) {
          el.focus()
        }
      },
    },
  },
})
</script>

<style lang="scss" scoped>
@import 'TodoList';

[v-cloak] {
  display: none;
}
</style>
