<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <BuildingAddForm :disabled="!project" @on-submit="onSubmit" />
      <BuildingFormList
        @on-update="onUpdateBuilding"
        @on-delete="onDeleteBuilding"
        :project="project"
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
import BuildingAddForm from '@/views/projects/Building/components/BuildingAddForm.vue'
import BuildingFormList from '@/views/projects/Building/components/BuildingFormList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'BuildingIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    BuildingAddForm,
    BuildingFormList,
  },
  created() {
    this.fetchBuildingList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') this.fetchBuildingList(target)
      else this.$store.state.project.buildingList = []
    },
    onSubmit(payload: any) {
      const project = this.project.pk
      this.createBuilding({ ...{ project }, ...payload })
    },
    onUpdateBuilding(payload: any) {
      const project = this.project.pk
      this.updateBuilding({ ...{ project }, ...payload })
    },
    onDeleteBuilding(pk: number) {
      const project = this.project.pk
      this.deleteBuilding({ ...{ pk }, ...{ project } })
    },
    ...mapActions('project', [
      'fetchBuildingList',
      'createBuilding',
      'updateBuilding',
      'deleteBuilding',
    ]),
  },
})
</script>
