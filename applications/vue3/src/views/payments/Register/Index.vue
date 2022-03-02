<template>
  <ContentHeader
      :page-title="pageTitle"
      :nav-menu="navMenu"
      @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContChoicer
          ref="listControl"
          :contract="contract"
          @list-filtering="onContFiltering"
          @get-contract="getContract"
      />
      <CRow>
        <CCol lg="7">
          <PayList :contract="contract"/>
          <PayForm/>
        </CCol>
        <CCol lg="5">
          <PayBoard :contract="contract"/>
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import HeaderMixin from '@/views/payments/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContChoicer from '@/views/payments/Register/components/ContChoicer.vue'
import PayList from '@/views/payments/Register/components/PayList.vue'
import PayForm from '@/views/payments/Register/components/PayForm.vue'
import PayBoard from '@/views/payments/Register/components/PayBoard.vue'
import {mapActions, mapGetters, mapState} from 'vuex'

export default defineComponent({
  name: 'PaymentsRegister',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContChoicer,
    PayList,
    PayForm,
    PayBoard,
  },
  created() {
    this.fetchTypeList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
    ...mapState('contract', ['contract']),
  },
  methods: {
    onContFiltering(payload: any) {
      const project = this.project.pk
      this.fetchContractList({...{project}, ...payload})
    },
    getContract(cont: number) {
      this.fetchContract(cont)
    },
    ...mapActions('project', ['fetchTypeList']),
    ...mapActions('contract', ['fetchContractList', 'fetchContract']),
  },
})
</script>
