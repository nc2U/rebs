<template>
  <ContentHeader
      :page-title="pageTitle"
      :nav-menu="navMenu"
      @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <DealDateForm/>
      <AddFormsTable
          :project="project"
          @on-update="onUpdate"
          @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter class="text-right">
      <CButton color="primary">일괄 등록하기</CButton>
    </CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import HeaderMixin from '@/views/proCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DealDateForm from '@/views/proCash/Register/components/DealDateForm.vue'
import AddFormsTable from '@/views/proCash/Register/components/AddFormsTable.vue'
import {mapActions, mapGetters, mapState} from 'vuex'

export default defineComponent({
  name: 'ProjectCashRegister',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    DealDateForm,
    AddFormsTable,
  },
  created() {
    this.fetchProFormAccD1List()
    this.fetchProFormAccD2List()
    this.fetchProBankAccList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    ...mapActions('proCash', [
      'fetchProFormAccD1List',
      'fetchProFormAccD2List',
      'fetchProBankAccList'
    ])
  }
})
</script>
