<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContChoicer ref="listControl" @payment-filtering="onPayFiltering" />
      <CRow>
        <CCol lg="6">
          <PayList />
          <PayForm />
        </CCol>
        <CCol lg="6">
          <PayBoard />
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/payments/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContChoicer from '@/views/payments/Register/components/ContChoicer.vue'
import PayList from '@/views/payments/Register/components/PayList.vue'
import PayForm from '@/views/payments/Register/components/PayForm.vue'
import PayBoard from '@/views/payments/Register/components/PayBoard.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

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
  },
  methods: {
    ...mapActions('project', ['fetchTypeList']),
  },
})
</script>
