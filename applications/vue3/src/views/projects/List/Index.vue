<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> 신규 프로젝트</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="['프로젝트 관리']" />

      <ProjectSelect :project="project" @on-change="onChange" />
    </CCardBody>
  </CCard>

  <component
    :is="compName"
    :userInfo="userInfo"
    :project="project"
    :update="update"
    @to-create="toCreate"
    @to-update="toUpdate"
    @reset-form="resetForm"
    @create-form="createForm"
    @update-form="updateForm"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import ProjectSelect from '@/components/ProjectSelect.vue'
import IndexForm from '@/views/projects/List/components/IndexForm.vue'
import IndexDetail from '@/views/projects/List/components/IndexDetail.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectsIndex',
  components: {
    HeaderNav,
    ProjectSelect,
    IndexForm,
    IndexDetail,
  },
  data() {
    return {
      compName: 'IndexForm',
      update: false,
    }
  },
  created() {
    this.fetchProject(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
    ...mapState('accounts', ['userInfo']),
  },
  watch: {
    project() {
      this.compName = 'IndexDetail'
    },
  },
  methods: {
    onChange(event: any) {
      this.fetchProject(event.target.value)
    },
    createForm() {
      this.update = false
      this.compName = 'IndexForm'
    },
    updateForm() {
      this.update = true
      this.compName = 'IndexForm'
    },
    resetForm() {
      this.update = false
      this.compName = 'IndexDetail'
    },
    toCreate(payload: any) {
      this.createProject(payload)
    },
    toUpdate(payload: any) {
      this.updateProject(payload)
    },
    ...mapActions('project', [
      'fetchProject',
      'createProject',
      'updateProject',
    ]),
  },
})
</script>
