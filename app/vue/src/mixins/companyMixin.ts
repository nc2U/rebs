import { defineComponent } from 'vue'
import { useCompany } from '@/store/pinia/company'

export default defineComponent({
  emits: ['header-select'],

  methods: {
    fetchCompany: (pk: string) => {
      useCompany().fetchCompany(pk)
    },
    comSelect(this: any, com: string) {
      if (!!com) this.fetchCompany(com)
      else useCompany().company = null
      this.$emit('header-select', com)
    },
  },
})
