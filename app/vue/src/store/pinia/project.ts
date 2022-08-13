import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useProject = defineStore('project', () => {
  // states
  const projectList = ref([])
  const project = ref(null)

  return {
    projectList,
    project,
  }
})
