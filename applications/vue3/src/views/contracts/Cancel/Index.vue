<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContNavigation />
      <ContController />
      <AddCancelCont />
      <CanceledList @page-select="pageSelect" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import AddCancelCont from '@/views/contracts/Cancel/components/AddCancelCont.vue'
import ContNavigation from '@/views/contracts/Cancel/components/ContNavigation.vue'
import ContController from '@/views/contracts/Cancel/components/ContController.vue'
import CanceledList from '@/views/contracts/Cancel/components/CanceledList.vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractCancel',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContNavigation,
    ContController,
    AddCancelCont,
    CanceledList,
  },
  created() {
    this.fetchContReleaseList({ project: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchContReleaseList({ project: target })
      } else {
        this.FETCH_CONT_RELEASE_LIST([])
      }
    },
    pageSelect(page: number) {
      const project = this.project.pk
      this.fetchContReleaseList({ project, page })
    },
    ...mapActions('contract', ['fetchContReleaseList']),
    ...mapMutations('contract', ['FETCH_CONT_RELEASE_LIST']),
  },
})
</script>
