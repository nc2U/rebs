import { defineComponent } from 'vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  data() {
    return {
      selected: true,
    }
  },
  created() {
    this.fetchProject(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    projSelect(event: any) {
      const target = event.target.value
      if (target !== '') {
        this.selected = true
        this.fetchProject(target)
      } else this.selected = false

      const selected = this.selected
      this.$emit('header-select', { target, selected })
    },
    ...mapActions('project', ['fetchProject']),
  },
})
