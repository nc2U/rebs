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
    projSelect(this: any, event: any) {
      const target = event.target.value
      if (target !== '') this.fetchProject(target)
      else this.$store.state.project.project = null

      this.$emit('header-select', target)
    },
    ...mapActions('project', ['fetchProject']),
  },
})
