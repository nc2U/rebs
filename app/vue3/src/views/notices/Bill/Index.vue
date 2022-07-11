<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <a href="/rebs/notice/bill/" target="_blank">
        구) 고지서 관리 페이지 바로가기
      </a>
      <SalesBillIssueForm />
      <ListController />
      <ContractList />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/notices/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import SalesBillIssueForm from '@/views/notices/Bill/components/SalesBillIssueForm.vue'
import ListController from '@/views/notices/Bill/components/ListController.vue'
import ContractList from '@/views/notices/Bill/components/ContractList.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Bill',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    SalesBillIssueForm,
    ListController,
    ContractList,
  },
  computed: {
    ...mapState('project', ['project']),
  },
})
</script>
