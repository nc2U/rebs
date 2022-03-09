<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <ContractForm @get-key-unit="getKeyUnit" />
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractForm from '@/views/contracts/Register/components/ContractForm.vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractRegister',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContractForm,
  },
  created() {
    this.fetchOrderGroupList(this.initProjId)
    this.fetchTypeList(this.initProjId)
    this.fetchKeyUnitList({ projct: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchOrderGroupList(target)
        this.fetchTypeList(target)
        this.fetchKeyUnitList({ project: target })
      } else {
        this.FETCH_ORDER_GROUP_LIST([])
        this.FETCH_TYPE_LIST([])
        this.FETCH_KEY_UNIT_LIST([])
      }
    },
    getKeyUnit(type: number) {
      const project = this.project.pk
      const unit_type = type
      this.fetchKeyUnitList({ project, unit_type, no_contract: true })
    },
    ...mapActions('contract', ['fetchOrderGroupList', 'fetchKeyUnitList']),
    ...mapActions('project', ['fetchTypeList']),
    ...mapMutations('contract', [
      'FETCH_ORDER_GROUP_LIST',
      'FETCH_KEY_UNIT_LIST',
    ]),
    ...mapMutations('project', ['FETCH_TYPE_LIST']),
  },
})
</script>
