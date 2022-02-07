import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  computed: {
    ...mapState('accounts', ['userInfo']),
  },
})
