import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useBudget = defineStore('budget', () => {
  // states

  const projectBudgetList = ref([])

  return {
    projectBudgetList,
  }
})
