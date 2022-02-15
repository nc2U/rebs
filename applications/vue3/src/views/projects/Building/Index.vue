<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <BuildingAddForm :disabled="!project" @on-submit="onSubmit" />
      <BuildingFormList
        @on-update="onUpdateBuilding"
        @on-delete="onDeleteBuilding"
        :project="project"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BuildingAddForm from '@/views/projects/Building/components/BuildingAddForm.vue'
import BuildingFormList from '@/views/projects/Building/components/BuildingFormList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'BuildingIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    BuildingAddForm,
    BuildingFormList,
  },
  created() {
    // this.fetchOrderGroupList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      // if (target !== '') this.fetchOrderGroupList(target)
      // else this.$store.state.contract.orderGroupList = []
    },
    onSubmit(payload: any) {
      const project = this.project.pk
      // this.createOrderGroup({ ...{ project }, ...payload })
    },
    onUpdateBuilding(payload: any) {
      const project = this.project.pk
      // this.updateOrderGroup({ ...{ project }, ...payload })
    },
    onDeleteBuilding(pk: number) {
      const project = this.project.pk
      // this.deleteOrderGroup({ ...{ pk }, ...{ project } })
    },
    // ...mapActions('contract', [
    // 'fetchOrderGroupList',
    // 'createOrderGroup',
    // 'updateOrderGroup',
    // 'deleteOrderGroup',
    // ]),
  },
})
</script>
