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
      <FloorAddForm :selected="selected" @on-submit="onSubmit" />
      <FloorFormList
        @on-update="onUpdateFloor"
        @on-delete="onDeleteFloor"
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
import ProjectSelect from '@/layouts/ContentHeader/ProjectSelect/Index.vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ProjectMixin from '@/views/projects/projectMixin'
import FloorAddForm from '@/views/projects/Floor/components/FloorAddForm.vue'
import { mapActions } from 'vuex'
import FloorFormList from '@/views/projects/Floor/components/FloorFormList.vue'

export default defineComponent({
  name: 'ProjectsFloorSet',
  mixins: [HeaderMixin, ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    FloorAddForm,
    FloorFormList,
  },
  created() {
    this.fetchFloorTypeList(this.initProjId)
  },
  methods: {
    projSelect(event: any) {
      if (event.target.value !== '') {
        this.selected = true
        this.fetchProject(event.target.value)
        this.fetchFloorTypeList(event.target.value)
      } else {
        this.selected = false
      }
    },
    onSubmit(payload: any) {
      const project = this.project.pk
      this.createFloorType({ ...{ project }, ...payload })
    },
    onUpdateFloor(payload: any) {
      const project = this.project.pk
      this.updateFloorType({ ...{ project }, ...payload })
    },
    onDeleteFloor(pk: number) {
      const project = this.project.pk
      this.deleteFloorType({ ...{ pk }, ...{ project } })
    },
    ...mapActions('project', [
      'fetchFloorTypeList',
      'createFloorType',
      'updateFloorType',
      'deleteFloorType',
    ]),
  },
})
</script>
