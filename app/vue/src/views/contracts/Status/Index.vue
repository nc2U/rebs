<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContSummary />
      <v-row>
        <v-col class="py-0">
          <ExcelExport v-if="project" :url="excelUrl" />
        </v-col>
      </v-row>
      <hr />
      <ContractBoard />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContSummary from '@/views/contracts/Status/components/ContSummary.vue'
import ExcelExport from '@/components/DownLoad/ExcelExport.vue'
import ContractBoard from '@/views/contracts/Status/components/ContractBoard.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractStatus',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContSummary,
    ExcelExport,
    ContractBoard,
  },
  created() {
    this.fetchTypeList(this.initProjId)
    this.fetchBuildingList(this.initProjId)
    this.fetchHouseUnitList({ project: this.initProjId })
  },
  computed: {
    excelUrl() {
      return this.project ? `excel/status/?project=${this.project.pk}` : ''
    },
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchTypeList(target)
        this.fetchBuildingList(target)
        this.fetchHouseUnitList({ project: target })
      } else {
        this.FETCH_TYPE_LIST([])
        this.FETCH_BUILDING_LIST([])
        this.FETCH_HOUSE_UNIT_LIST([])
      }
    },
    ...mapActions('project', [
      'fetchTypeList',
      'fetchBuildingList',
      'fetchHouseUnitList',
    ]),
    ...mapGetters('project', [
      'FETCH_TYPE_LIST',
      'FETCH_BUILDING_LIST',
      'FETCH_HOUSE_UNIT_LIST',
    ]),
  },
})
</script>
