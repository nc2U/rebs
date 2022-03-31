<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContNavigation :contractor="contractor" />
      <ContController />
      <CAlert v-if="contractor" color="info">{{ contractor }}</CAlert>
      <AddCancelCont @on-submit="onSubmit" />
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
  created(this: any) {
    this.fetchContReleaseList({ project: this.initProjId })
    if (this.$route.query.contractor)
      this.fetchContractor(this.$route.query.contractor)
    else this.FETCH_CONTRACTOR(null)
  },
  beforeRouteLeave() {
    this.FETCH_CONTRACTOR(null)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapState('contract', ['contractor']),
    ...mapGetters('accounts', ['initProjId']),
  },
  watch: {
    $route(val) {
      if (val.query.contractor) this.fetchContractor(val.query.contractor)
      else this.FETCH_CONTRACTOR(null)
    },
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchContReleaseList({ project: target })
      } else {
        this.FETCH_CONTRACTOR(null)
        this.FETCH_CONT_RELEASE_LIST([])
      }
    },
    pageSelect(page: number) {
      const project = this.project.pk
      this.fetchContReleaseList({ project, page })
    },
    onSubmit(payload: any) {
      alert('ok~~~!')
      console.log(payload)
    },
    ...mapActions('contract', ['fetchContractor', 'fetchContReleaseList']),
    ...mapMutations('contract', [
      'FETCH_CONTRACTOR',
      'FETCH_CONT_RELEASE_LIST',
    ]),
  },
})
</script>
