<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <DateChoicer />

      <TabSelect @tab-select="showTab" />

      <component :is="compName" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/proCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/proCash/Status/components/DateChoicer.vue'
import TabSelect from '@/views/proCash/Status/components/TabSelect.vue'
import StatusByAccount from '@/views/proCash/Status/components/StatusByAccount.vue'
import CashListByDate from '@/views/proCash/Status/components/CashListByDate.vue'
import SummaryForBudget from '@/views/proCash/Status/components/SummaryForBudget.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectCashStatus',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    DateChoicer,
    TabSelect,
    StatusByAccount,
    CashListByDate,
    SummaryForBudget,
  },
  data() {
    return {
      compName: 'StatusByAccount',
    }
  },
  computed: {
    ...mapState('project', ['project']),
  },
  methods: {
    showTab(num: number) {
      if (num === 1) this.compName = 'StatusByAccount'
      else if (num === 2) this.compName = 'CashListByDate'
      else if (num === 3) this.compName = 'SummaryForBudget'
    },
  },
})
</script>
