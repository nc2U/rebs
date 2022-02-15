<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <BuildingSelector :disabled="!project" @on-submit="onSubmit" />
      <!--      <TypeFormList-->
      <!--        @on-update="onUpdateType"-->
      <!--        @on-delete="onDeleteType"-->
      <!--        :project="project"-->
      <!--      />-->
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
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'UnitIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    BuildingSelector,
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
