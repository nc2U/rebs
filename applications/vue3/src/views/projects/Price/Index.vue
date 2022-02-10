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

    <CCardBody class="pb-5">
      <PriceSelectForm
        ref="formSelect"
        @on-order-select="orderSelect"
        @on-type-select="typeSelect"
        :selected="selected"
        :orders="orderGroupList"
        :types="unitTypeList"
      />
      <PriceFormList
        @on-create="onCreatePrice"
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
      order_group: '', // condTexts 함수에 인자로 사용
      unit_type: '',
      queryIds: {},
      priceMessage: '공급가격을 입력하기 위해 [차수 정보]를 선택하여 주십시요.',
    }
  },
  created() {
    // 항상 실행
    this.fetchOrderGroupList(this.initProjId)
    this.fetchTypeList(this.initProjId)
    this.fetchFloorTypeList(this.initProjId)
  },
  computed: {
    condTexts() {
      // 차수명과 타입명 구하기
      const orderText = this.orderGroupList
        .filter((o: any) => o.pk == this.order_group)
        .map((o: any) => o.order_group_name)[0]
      const typeText = this.unitTypeList
        .filter((t: any) => t.pk == this.unit_type)
        .map((t: any) => t.name)[0]
      return { orderText, typeText }
    },
    // created 훅에서 실행한 fetch 관련 상태 가져오기
    ...mapState('contract', ['orderGroupList']),
    ...mapState('project', ['unitTypeList', 'floorTypeList']),
  },
  methods: {
    // projectSelect change 이벤트시 실행 함수
    projSelect(this: any, event: any) {
      if (event.target.value !== '') {
        // 프로젝트 선택시
        this.selected = true
        this.fetchProject(event.target.value)
        this.fetchOrderGroupList(event.target.value)
        this.fetchTypeList(event.target.value)
        this.fetchFloorTypeList(event.target.value)
        this.$refs.formSelect.orderDisabled = false
      } else {
        // 프로젝트 선택 해제시
        this.selected = false
        this.$refs.formSelect.orderDisabled = true
      }
      // 프로젝트 change 이벤트 발생 시 항상 실행
      this.resetPrices() // 가격 상태 초기화
      this.orderSelect('') // 차수 선택 초기화
      this.$refs.formSelect.order = '' // 차수 선택 값 초기화
      this.$refs.formSelect.type = '' // 타입 선택 값 초기화
    },
    // 차수 선택 시 실행 함수
    orderSelect(payload: any) {
      this.order_group = payload // order_group pk 값 할당
      this.priceMessage =
        payload == ''
          ? '공급가격을 입력하기 위해 [차수 정보]를 선택하여 주십시요.'
          : '공급가격을 입력하기 위해 [타입 정보]를 선택하여 주십시요.'
      this.resetPrices() // 가격 상태 초기화
    },
    // 타입 선택 시 실행 함수
    typeSelect(payload: any) {
      this.unit_type = payload // unit_type pk 값 할당
      this.priceMessage =
        payload == ''
          ? '공급가격을 입력하기 위해 [타입 정보]를 선택하여 주십시요.'
          : ''
      const project = String(this.project.pk)
      const order_group = this.order_group
      const unit_type = this.unit_type
      const queryIds = { project, order_group, unit_type }
      this.queryIds = queryIds // this.queryIds 값 할당
      this.fetchPriceList(queryIds) // 갸격 상태 저장 실행
    },
    // 프로젝트 또는 차수 선택 변경 시 가격 데이터 초기화
    resetPrices(this: any) {
      this.$store.state.cash.priceList = []
    },

    onCreatePrice(payload: any) {
      alert('create!')
      console.log(payload)
    },
    onUpdatePrice(payload: any) {
      this.updatePrice(payload)
    },
    onDeletePrice(pk: any) {
      alert(pk)
    },
    ...mapActions('contract', ['fetchOrderGroupList']),
    ...mapActions('project', ['fetchTypeList', 'fetchFloorTypeList']),
    ...mapActions('cash', [
      'fetchPriceList',
      'fetchPrice',
      'createPrice',
      'updatePrice',
    ]),
  },
})
</script>
