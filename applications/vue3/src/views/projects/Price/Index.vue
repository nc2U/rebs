<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <ProjectSelect :project="project" @proj-select="projSelect" />
    </CCardBody>
  </CCard>

  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-notes" />
      <strong class="pl-1"> {{ $route.name }}</strong>
    </CCardHeader>

    <CCardBody class="pb-5" v-if="project">
      <PriceSelectForm
        @on-order-select="orderSelect"
        @on-type-select="typeSelect"
        @on-floor-select="floorSelect"
        :selected="selected"
        :orders="orderGroupList"
        :types="unitTypeList"
      />
      <PriceFormList
        @on-update="onUpdatePrice"
        @on-delete="onDeletePrice"
        :selected="selected"
        :msg="priceMessage"
        :cond-texts="condTexts"
        :query-ids="queryIds"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import ProjectSelect from '@/components/ProjectSelect/Index.vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ProjectMixin from '@/views/projects/projectMixin'
import PriceSelectForm from '@/views/projects/Price/components/PriceSelectForm.vue'
import PriceFormList from '@/views/projects/Price/components/PriceFormList.vue'
import { mapActions, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectsPriceSet',
  mixins: [HeaderMixin, ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    PriceSelectForm,
    PriceFormList,
  },
  data() {
    return {
      orderPk: '',
      typePk: '',
      floorPk: '',
      queryIds: {},
      priceMessage: '공급가격을 입력하기 위해 [차수 정보]를 선택하여 주십시요.',
    }
  },
  created() {
    this.fetchOrderGroupList(this.initProjId)
    this.fetchTypeList(this.initProjId)
  },
  computed: {
    condTexts() {
      const orderText = this.orderGroupList
        .filter((o: any) => o.pk == this.orderPk)
        .map((o: any) => o.order_group_name)[0]
      const typeText = this.unitTypeList
        .filter((t: any) => t.pk == this.typePk)
        .map((t: any) => t.name)[0]
      return { orderText, typeText }
    },
    ...mapState('contract', ['orderGroupList']),
    ...mapState('project', ['unitTypeList', 'floorTypeList']),
  },
  methods: {
    projSelect(event: any) {
      if (event.target.value !== '') {
        this.selected = true
        this.fetchProject(event.target.value)
        this.fetchOrderGroupList(event.target.value)
        this.fetchTypeList(event.target.value)
      } else {
        this.selected = false
      }
      this.resetPrices()
    },
    orderSelect(payload: any) {
      this.orderPk = payload
      this.priceMessage =
        payload == ''
          ? '공급가격을 입력하기 위해 [차수 정보]를 선택하여 주십시요.'
          : '공급가격을 입력하기 위해 [타입 정보]를 선택하여 주십시요.'
      this.resetPrices()
    },
    typeSelect(payload: any) {
      this.typePk = payload
      this.priceMessage =
        payload == ''
          ? '공급가격을 입력하기 위해 [타입 정보]를 선택하여 주십시요.'
          : ''
      const projId = String(this.project.pk)
      const orderId = this.orderPk
      const typeId = this.typePk
      const queryIds = { projId, orderId, typeId }
      this.queryIds = queryIds
      this.fetchPriceList(queryIds)
      this.fetchFloorTypeList(projId)
    },
    resetPrices(this: any) {
      this.$store.state.project.floorTypeList = []
      this.$store.state.cash.priceList = []
    },
    ...mapActions('contract', ['fetchOrderGroupList']),
    ...mapActions('project', ['fetchTypeList', 'fetchFloorTypeList']),
    ...mapActions('cash', ['fetchPriceList', 'fetchPrice']),
  },
})
</script>
