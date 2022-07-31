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
        @get-release="getRelease"
      />
      <ContractorAlert v-if="contractor" :contractor="contractor" />
      <ReleasetButton
        v-if="contractor"
        :contractor="contractor"
        @on-submit="onSubmit"
      />
      <TableTitleRow
        v-if="project"
        title="계약해지 현황"
        color="error"
        excel
        :url="downloadUrl"
      />
      <ReleaseList
        @page-select="pageSelect"
        @get-release="getRelease"
        @on-submit="onSubmit"
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
import TableTitleRow from '@/components/TableTitleRow.vue'
import ReleaseList from '@/views/contracts/Release/components/ReleaseList.vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'ReleaseIndex',
  components: {
    ContentHeader,
    ContentBody,
    ContNavigation,
    ContractorAlert,
    ContController,
    ReleasetButton,
    TableTitleRow,
    ReleaseList,
  },
  mixins: [HeaderMixin],
  beforeRouteLeave() {
    this.FETCH_CONTRACTOR(null)
  },
  data() {
    return {
      page: 1,
    }
  },
  created(this: any) {
    this.fetchContReleaseList({ project: this.initProjId })
    if (this.$route.query.contractor)
      this.fetchContractor(this.$route.query.contractor)
    else this.FETCH_CONTRACTOR(null)
  },
  computed: {
    downloadUrl() {
      return `/excel/releases/?project=${this.project.pk}`
    },
    ...mapState('project', ['project']),
    ...mapState('contract', ['contractor']),
    ...mapGetters('accounts', ['initProjId']),
  },
  watch: {
    $route(val) {
      if (val.query.contractor) this.fetchContractor(val.query.contractor)
      else this.FETCH_CONTRACTOR(null)
    },
    contractor(val) {
      if (val && val.contractorrelease) {
        this.fetchContRelease(val.contractorrelease)
      }
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
      if (search !== '') {
        const project = this.project.pk
        this.fetchContractorList({ project, search })
      } else this.FETCH_CONTRACTOR_LIST([])
    },
    getRelease(release: number) {
      this.fetchContRelease(release)
    },
    pageSelect(page: number) {
      this.page = page
      const project = this.project.pk
      this.fetchContReleaseList({ project, page })
    },
    onSubmit(payload: any) {
      const page = this.page
      const project = this.project.pk
      if (payload.pk) this.updateRelease({ project, page, ...payload })
      else this.createRelease({ project, ...payload })
    },
    ...mapActions('contract', [
      'fetchContractor',
      'fetchContractorList',
      'fetchContRelease',
      'fetchContReleaseList',
      'createRelease',
      'updateRelease',
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
