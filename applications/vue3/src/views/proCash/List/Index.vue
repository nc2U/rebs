<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @payment-filtering="onPayFiltering" />
      <ProCashList
        :project="project"
        @page-select="pageSelect"
        @on-update="onUpdate"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/proCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/proCash/List/components/ListController.vue'
import ProCashList from '@/views/proCash/List/components/ProCashList.vue'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectCashList',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ListController,
    ProCashList,
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
})
</script>
