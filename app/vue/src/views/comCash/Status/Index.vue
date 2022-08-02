<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { pageTitle, navMenu } from '@/views/comCash/_menu/headermixin'
import { dateFormat } from '@/utils/baseMixins'

import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/comCash/Status/components/DateChoicer.vue'
import TabSelect from '@/views/comCash/Status/components/TabSelect.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import StatusByAccount from '@/views/comCash/Status/components/StatusByAccount.vue'
import CashListByDate from '@/views/comCash/Status/components/CashListByDate.vue'

export default defineComponent({
  name: 'CashesStatus',
  components: {
    ContentHeader,
    ContentBody,
    DateChoicer,
    TabSelect,
    TableTitleRow,
    StatusByAccount,
    CashListByDate,
  },
  setup() {
    const store = useStore()
    const date = ref(new Date())
    const compName = ref('StatusByAccount')

    const company = computed(() => store.state.settings.company)
    const initComId = computed(() => store.getters['accounts/initComId'])

    const fetchAllAccD1List = () => store.dispatch('comCash/fetchAllAccD1List')
    const fetchAllAccD2List = () => store.dispatch('comCash/fetchAllAccD2List')
    const fetchAllAccD3List = () => store.dispatch('comCash/fetchAllAccD3List')
    const fetchComBankAccList = (com: number) =>
      store.dispatch('comCash/fetchComBankAccList', com)
    const fetchComBalanceByAccList = (com: { company: number }) =>
      store.dispatch('comCash/fetchComBalanceByAccList', com)
    const fetchDateCashBookList = (payload: any) =>
      store.dispatch('comCash/fetchDateCashBookList', payload)

    const updateState = (payload: any) =>
      store.commit('comCash/updateState', payload)

    const onSelectAdd = (target: any) => {
      if (target !== '') {
        fetchComBankAccList(target)
        fetchComBalanceByAccList({ company: target })
        fetchDateCashBookList({
          company: target,
          date: dateFormat(date.value),
        })
      } else {
        updateState({
          comBankList: [],
          comBalanceByAccList: [],
          dateCashBook: [],
        })
      }
    }

    const showTab = (num: number) => {
      const comp: { [key: number]: string } = {
        1: 'StatusByAccount',
        2: 'CashListByDate',
      }
      compName.value = comp[num]
    }

    const setDate = (d: string) => {
      const dt = new Date(d)
      date.value = new Date(dt)
      fetchComBalanceByAccList({ company: company.value.pk })
      fetchDateCashBookList({
        company: company.value.pk,
        date: dateFormat(dt),
      })
    }

    onMounted(() => {
      fetchAllAccD1List()
      fetchAllAccD2List()
      fetchAllAccD3List()
      fetchComBankAccList(initComId.value)
      fetchComBalanceByAccList({ company: initComId.value })
      fetchDateCashBookList({
        company: initComId.value,
        date: dateFormat(date.value),
      })
    })

    return {
      date,
      compName,
      pageTitle,
      navMenu,
      onSelectAdd,
      showTab,
      setDate,
    }
  },
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="CompanySelect"
    @header-select="onSelectAdd"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <DateChoicer @set-date="setDate" />

      <TabSelect @tab-select="showTab" />

      <TableTitleRow excel disabled />

      <component :is="compName" :date="date" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
