import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useSite = defineStore('project', () => {
  // states

  const siteList = ref([])
  const siteOwnerList = ref([])
  const siteOwnerRelationList = ref([])
  const siteContractList = ref([])

  return {
    siteList,
    siteOwnerList,
    siteOwnerRelationList,
    siteContractList,
  }
})
