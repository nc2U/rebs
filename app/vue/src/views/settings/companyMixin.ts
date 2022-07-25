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
    comSelect(this: any, event: any) {
      const target = event.target.value
      if (target !== '') this.fetchCompany(target)
      else this.$store.state.settings.company = null

      this.$emit('header-select', target)
    },
    ...mapActions('settings', ['fetchCompany']),
  },
})
