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
    comSelect(event: any) {
      const target = event.target.value
      if (target !== '') this.fetchCompany(target)

      this.$emit('header-select', target)
    },
    ...mapActions('settings', ['fetchCompany']),
  },
})
