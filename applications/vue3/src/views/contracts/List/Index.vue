<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <ProjectSelect :project="project" @on-change="onChange" />
      <IndexSummary :project="project" />
    </CCardBody>
  </CCard>

  <component :is="compName" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import ProjectSelect from '@/components/ProjectSelect.vue'
import IndexSummary from './components/IndexSummary.vue'
import IndexList from './components/IndexList.vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin1'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractIndex',
  mixins: [HeaderMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    IndexSummary,
    IndexList,
  },
  data() {
    return {
      compName: 'IndexList',
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
