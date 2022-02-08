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
      if (event.target.value !== '') {
        this.selected = true
        this.fetchProject(event.target.value)
      } else {
        this.selected = false
      }
    },
    ...mapActions('project', ['fetchProject']),
  },
})
