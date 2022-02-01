<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> 현장 문서관리</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="['현장 일반문서']" />

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
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectGeneralDocs',
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
