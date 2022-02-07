import { defineComponent } from 'vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  created() {
    this.fetchCompany(this.initComId)
  },
  computed: {
    ...mapState('settings', ['company']),
    ...mapGetters('accounts', ['initComId']),
  },
  methods: {
    comSelect(event: any) {
      this.fetchCompany(event.target.value)
    },
    ...mapActions('settings', ['fetchCompany']),
  },
})
