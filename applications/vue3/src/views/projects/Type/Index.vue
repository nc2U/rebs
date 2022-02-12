<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <TypeAddForm @on-submit="onSubmit" />
      <TypeFormList
        @on-update="onUpdateType"
        @on-delete="onDeleteType"
        :project="project"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import TypeAddForm from '@/views/projects/Type/components/TypeAddForm.vue'
import TypeFormList from '@/views/projects/Type/components/TypeFormList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectsTypeSet',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    TypeAddForm,
    TypeFormList,
  },
  created() {
    this.fetchTypeList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') this.fetchTypeList(target)
      else this.$store.state.project.unitTypeList = []
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
