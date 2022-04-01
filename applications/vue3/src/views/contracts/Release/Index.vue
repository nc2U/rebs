<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContNavigation :contractor="contractor" />
      <ContController
        @search-contractor="searchContractor"
        @update-confirm="updateConfirm"
      />
      <ContractorAlert v-if="contractor" :contractor="contractor" />
      <ReleasetButton
        v-if="contractor"
        :contractor="contractor"
        @on-submit="onCreate"
      />
      <ReleaseList
        @page-select="pageSelect"
        @update-confirm="updateConfirm"
        @on-submit="onUpdate"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ReleasetButton from '@/views/contracts/Release/components/ReleasetButton.vue'
import ContNavigation from '@/views/contracts/Release/components/ContNavigation.vue'
import ContractorAlert from '@/views/contracts/Release/components/ContractorAlert.vue'
import ContController from '@/views/contracts/Release/components/ContController.vue'
import ReleaseList from '@/views/contracts/Release/components/ReleaseList.vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'ReleaseIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContNavigation,
    ContractorAlert,
    ContController,
    ReleasetButton,
    ReleaseList,
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
        this.FETCH_CONTRACTOR_LIST([])
        this.FETCH_CONT_RELEASE(null)
        this.FETCH_CONT_RELEASE_LIST([])
      }
      this.$router.push({ name: '계약해지 관리' })
    },
    searchContractor(search: string) {
      const project = this.project.pk
      this.fetchContractorList({ project, search })
    },
    updateConfirm(release: number) {
      this.fetchContRelease(release)
    },
    pageSelect(page: number) {
      const project = this.project.pk
      this.fetchContReleaseList({ project, page })
    },
    onCreate(payload: any) {
      alert('ok~~create~!')
      console.log(payload)
    },
    onUpdate(payload: any) {
      alert('ok~~update~!')
      console.log(payload)
    },
    ...mapActions('contract', [
      'fetchContractor',
      'fetchContractorList',
      'fetchContRelease',
      'fetchContReleaseList',
    ]),
    ...mapMutations('contract', [
      'FETCH_CONTRACTOR',
      'FETCH_CONTRACTOR_LIST',
      'FETCH_CONT_RELEASE',
      'FETCH_CONT_RELEASE_LIST',
    ]),
  },
})
</script>
