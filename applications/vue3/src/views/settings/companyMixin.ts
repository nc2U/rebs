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
      const target = event.target.value
      if (target !== '') {
        this.selected = true
        this.fetchCompany(target)
      } else this.selected = false

      const selected = this.selected
      this.$emit('header-select', { target, selected })
    },
    ...mapActions('settings', ['fetchCompany']),
  },
})
