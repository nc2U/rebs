import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useBudget = defineStore('project', () => {
  // states

  const projectBudgetList = ref([])

  return {
    projectBudgetList,
  }
})
