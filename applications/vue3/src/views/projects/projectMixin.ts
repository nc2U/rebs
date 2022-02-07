import { defineComponent } from 'vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  created() {
    this.fetchProject(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    projSelect(event: any) {
      this.fetchProject(event.target.value)
    },
    ...mapActions('project', ['fetchProject']),
  },
})
