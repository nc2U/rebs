<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <ProjectSelect :project="project" @on-change="onChange" />
    </CCardBody>
  </CCard>

  <component :is="compName" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import ProjectSelect from '@/components/ProjectSelect.vue'
import BlankComponent from '@/components/BlankComponent.vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin2'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractRegister',
  mixins: [HeaderMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    BlankComponent,
  },
  data() {
    return {
      compName: 'BlankComponent',
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
    onChange(event: any) {
      this.fetchProject(event.target.value)
    },
    ...mapActions('project', ['fetchProject']),
  },
})
</script>
