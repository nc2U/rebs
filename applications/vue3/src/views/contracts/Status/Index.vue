<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContSummary />
      <ExcelExport />
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
import ExcelExport from '@/views/contracts/Status/components/ExcelExport.vue'
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
    this.fetchHouseUnitList({ project: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        // this.fetchOrderGroupList(target)
        // this.fetchTypeList(target)
        // this.fetchKeyUnitList({ project: target })
        // this.fetchHouseUnitList({ project: target })
        // this.fetchProBankAccList(target)
        // this.fetchPayOrderList(target)
      } else {
        // this.FETCH_ORDER_GROUP_LIST([])
        // this.FETCH_TYPE_LIST([])
        // this.FETCH_KEY_UNIT_LIST([])
        // this.FETCH_HOUSE_UNIT_LIST([])
        // this.FETCH_P_BANK_ACCOUNT_LIST([])
        // this.FETCH_PAY_ORDER_LIST([])
      }
    },
    ...mapActions('project', ['fetchHouseUnitList']),
  },
})
</script>
