<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <ProjectSelect :project="project" @proj-select="projSelect" />
    </CCardBody>
  </CCard>

  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-notes" />
      <strong class="pl-1"> {{ $route.name }}</strong>
    </CCardHeader>

    <CCardBody class="pb-5" v-if="project">
      <TypeAddForm :selected="selected" @on-submit="onSubmit" />
      <TypeFormList
        @on-update="onUpdateType"
        @on-delete="onDeleteType"
        :selected="selected"
        :project="project"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import ProjectSelect from '@/components/ProjectSelect/Index.vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ProjectMixin from '@/views/projects/projectMixin'
import TypeAddForm from '@/views/projects/Type/components/TypeAddForm.vue'
import TypeFormList from '@/views/projects/Type/components/TypeFormList.vue'
import { mapActions } from 'vuex'

export default defineComponent({
  name: 'ProjectsTypeSet',
  mixins: [HeaderMixin, ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    TypeAddForm,
    TypeFormList,
  },
  created() {
    this.fetchTypeList(this.initProjId)
  },
  methods: {
    projSelect(event: any) {
      if (event.target.value !== '') {
        this.selected = true
        this.fetchProject(event.target.value)
        this.fetchTypeList(event.target.value)
      } else {
        this.selected = false
      }
    },
    onSubmit(payload: any) {
      const project = this.project.pk
      this.createType({ ...{ project }, ...payload })
    },
    onUpdateType(payload: any) {
      const project = this.project.pk
      this.updateType({ ...{ project }, ...payload })
    },
    onDeleteType(pk: number) {
      const project = this.project.pk
      this.deleteType({ ...{ pk }, ...{ project } })
    },
    ...mapActions('project', [
      'fetchTypeList',
      'createType',
      'updateType',
      'deleteType',
    ]),
  },
})
</script>
