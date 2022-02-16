<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <BuildingSelector :project="project" @on-submit="onSubmit" />
      <UnitListTable :project="project" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BuildingSelector from '@/views/projects/Unit/components/BuildingSelector.vue'
import UnitListTable from '@/views/projects/Unit/components/UnitListTable.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'UnitIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    BuildingSelector,
    UnitListTable,
  },
  created() {
    this.fetchTypeList(this.initProjId)
    this.fetchBuildingList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchBuildingList(target)
        this.fetchTypeList(target)
      } else {
        this.$store.state.project.unitTypeList = []
        this.$store.state.project.buildingList = []
      }
    },
    ...mapActions('project', ['fetchTypeList', 'fetchBuildingList']),
  },
})
</script>
