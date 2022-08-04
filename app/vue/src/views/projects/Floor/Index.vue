<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <FloorAddForm :disabled="!project" @on-submit="onSubmit" />
      <FloorFormList
        :project="project"
        @on-update="onUpdateFloor"
        @on-delete="onDeleteFloor"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import FloorAddForm from '@/views/projects/Floor/components/FloorAddForm.vue'
import { mapActions, mapGetters, mapState } from 'vuex'
import FloorFormList from '@/views/projects/Floor/components/FloorFormList.vue'

export default defineComponent({
  name: 'ProjectsFloorSet',
  components: {
    ContentHeader,
    ContentBody,
    FloorAddForm,
    FloorFormList,
  },
  mixins: [HeaderMixin],
  created() {
    this.fetchFloorTypeList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') this.fetchFloorTypeList(target)
      else this.$store.state.project.floorTypeList = []
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
