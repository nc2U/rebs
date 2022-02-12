import { defineComponent } from 'vue'
import { mapActions, mapGetters } from 'vuex'

export default defineComponent({
  data() {
    return {
      selected: true,
    }
  },
  created() {
    this.fetchCompany(this.initComId)
  },
  computed: {
    ...mapGetters('accounts', ['initComId']),
  },
  methods: {
    comSelect(event: any) {
      if (event.target.value !== '') {
        this.selected = true
        this.fetchCompany(event.target.value)
      } else {
        this.selected = false
      }
    },
    ...mapActions('settings', ['fetchCompany']),
  },
})
