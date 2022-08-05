import { defineComponent } from 'vue'
import { mapActions, mapGetters } from 'vuex'

export default defineComponent({
  created() {
    this.fetchCompany(this.initComId)
  },
  computed: {
    ...mapGetters('accounts', ['initComId']),
  },
  methods: {
    comSelect(this: any, com: string) {
      if (com !== '') this.fetchCompany(com)
      else this.$store.commit('settings/updateState', { company: null })

      this.$emit('header-select', com)
    },
    ...mapActions('settings', ['fetchCompany']),
  },
})
