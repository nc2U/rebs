<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <ContractForm
      :contract="contract"
      :unit-set="unitSet"
      :is-union="isUnion"
      @type-select="typeSelect"
      @on-create="onCreate"
      @on-update="onUpdate"
    />
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin'
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
  created(this: any) {
    this.fetchOrderGroupList(this.initProjId)
    this.fetchTypeList(this.initProjId)

    this.fetchProBankAccList(this.initProjId)
    this.fetchPayOrderList(this.initProjId)

    this.fetchKeyUnitList({ project: this.initProjId })
    this.fetchHouseUnitList({ project: this.initProjId })

    if (this.$route.query.contract) {
      this.getContract(this.$route.query.contract)
    }
  },
  computed: {
    unitSet() {
      return this.project ? this.project.is_unit_set : false
    },
    isUnion() {
      return this.project ? !this.project.is_direct_manage : false
    },
    ...mapState('contract', ['contract']),
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  watch: {
    contract(newVal) {
      if (this.contract) {
        this.fetchKeyUnitList({
          project: this.project ? this.project.pk : this.initProjId,
          unit_type: newVal.unit_type.pk,
          contract: this.$route.query.contract,
          available: 'false',
        })

        if (this.contract.keyunit.houseunit) {
          this.fetchHouseUnitList({
            project: this.project ? this.project.pk : this.initProjId,
            unit_type: newVal.unit_type.pk,
            contract: this.$route.query.contract,
            available: 'false',
          })
        } else {
          this.fetchHouseUnitList({
            project: this.project ? this.project.pk : this.initProjId,
            unit_type: newVal.unit_type.pk,
          })
        }
      }
    },
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchOrderGroupList(target)
        this.fetchTypeList(target)
        this.fetchKeyUnitList({ project: target })
        this.fetchHouseUnitList({ project: target })
        this.fetchProBankAccList(target)
        this.fetchPayOrderList(target)
      } else {
        this.FETCH_ORDER_GROUP_LIST([])
        this.FETCH_TYPE_LIST([])
        this.FETCH_KEY_UNIT_LIST([])
        this.FETCH_HOUSE_UNIT_LIST([])
        this.FETCH_P_BANK_ACCOUNT_LIST([])
        this.FETCH_PAY_ORDER_LIST([])
      }
    },
    typeSelect(type: number) {
      const project = this.project.pk
      const unit_type = type
      this.fetchKeyUnitList({ project, unit_type })
      this.fetchHouseUnitList({ project, unit_type })
    },
    getContract(cont: number) {
      this.fetchContract(cont)
    },
    onCreate(payload: any) {
      const project = this.project.pk
      this.createContractSet({ project, ...payload })
      this.$router.push({ name: '계약내역 조회' })
    },
    onUpdate(payload: any) {
      alert('ok! - update!')
      console.log(payload)
    },
    ...mapActions('contract', [
      'fetchOrderGroupList',
      'fetchKeyUnitList',
      'fetchHouseUnitList',
      'createContractSet',
      'fetchContract',
    ]),
    ...mapActions('project', ['fetchTypeList']),
    ...mapActions('proCash', ['fetchProBankAccList']),
    ...mapActions('payment', ['fetchPayOrderList']),
    ...mapMutations('contract', [
      'FETCH_ORDER_GROUP_LIST',
      'FETCH_KEY_UNIT_LIST',
      'FETCH_HOUSE_UNIT_LIST',
    ]),
    ...mapMutations('proCash', ['FETCH_P_BANK_ACCOUNT_LIST']),
    ...mapMutations('project', ['FETCH_TYPE_LIST']),
    ...mapMutations('payment', ['FETCH_PAY_ORDER_LIST']),
  },
})
</script>
