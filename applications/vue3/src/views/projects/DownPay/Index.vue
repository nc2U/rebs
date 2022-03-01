<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <DownPayAddForm
        :disabled="!project"
        :orders="orderGroupList"
        :types="unitTypeList"
        @on-submit="onSubmit"
      />
      <DownPayFormList
        @on-update="onUpdateDownPay"
        @on-delete="onDeleteDownPay"
        :orders="orderGroupList"
        :types="unitTypeList"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DownPayAddForm from '@/views/projects/DownPay/components/DownPayAddForm.vue'
import DownPayFormList from '@/views/projects/DownPay/components/DownPayFormList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectsDownPaySet',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    DownPayAddForm,
    DownPayFormList,
  },
  created() {
    this.fetchDownPayList(this.initProjId)
    this.fetchOrderGroupList(this.initProjId)
    this.fetchTypeList(this.initProjId)
  },
  computed: {
    ...mapState('contract', ['orderGroupList']),
    ...mapState('project', ['project', 'unitTypeList']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchOrderGroupList(target)
        this.fetchTypeList(target)
        this.fetchDownPayList(target)
      } else this.$store.state.payment.downPayList = []
    },
    onSubmit(payload: any) {
      const project = this.project.pk
      this.createDownPay({ ...{ project }, ...payload })
    },
    onUpdateDownPay(payload: any) {
      const project = this.project.pk
      this.updateDownPay({ ...{ project }, ...payload })
    },
    onDeleteDownPay(pk: number) {
      const project = this.project.pk
      this.deleteDownPay({ ...{ pk }, ...{ project } })
    },
    ...mapActions('payment', [
      'fetchDownPayList',
      'createDownPay',
      'updateDownPay',
      'deleteDownPay',
    ]),
    ...mapActions('contract', ['fetchOrderGroupList']),
    ...mapActions('project', ['fetchTypeList']),
  },
})
</script>
