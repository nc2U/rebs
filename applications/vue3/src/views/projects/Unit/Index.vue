<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <UnitController
        :project="project"
        @bldg-select="bldgSelect"
        @unit-register="unitRegister"
      />
      <UnitListTable :bldg-name="bldgName" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UnitController from '@/views/projects/Unit/components/UnitController.vue'
import UnitListTable from '@/views/projects/Unit/components/UnitListTable.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'UnitIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    UnitController,
    UnitListTable,
  },
  data() {
    return {
      bldgName: '',
    }
  },
  created(this: any) {
    this.fetchTypeList(this.initProjId)
    this.fetchFloorTypeList(this.initProjId)
    this.fetchBuildingList(this.initProjId)
    this.$store.state.project.houseUnitList = []
  },
  computed: {
    ...mapState('project', ['project', 'floorTypeList']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchTypeList(target)
        this.fetchFloorTypeList(target)
        this.fetchBuildingList(target)
      } else {
        this.$store.state.project.unitTypeList = []
        this.$store.state.project.floorTypeList = []
        this.$store.state.project.buildingList = []
      }
      this.$store.state.project.houseUnitList = []
    },
    bldgSelect(this: any, bldg: any) {
      if (bldg.pk !== '')
        this.fetchUnitList({ project: this.project.pk, bldg: bldg.pk })
      else this.$store.state.project.houseUnitList = []
      this.bldgName = bldg.name
    },
    unitRegister(payload: any) {
      const project = this.project.pk
      const unit_type = Number(payload.type)
      const building_unit = Number(payload.building)
      const bldg_line = payload.line
      const middleWord = bldg_line < 10 ? '0' : ''
      const size = payload.maxFloor - payload.minFloor + 1
      const range = (size: number, min: number): number[] =>
        [...Array(size).keys()].map(key => key + min)
      const between = (x: number, min: number, max: number): boolean =>
        x >= min && x <= max
      const floors = range(size, payload.minFloor).map(i => ({
        floor_no: i,
        name: `${i}${middleWord}${bldg_line}`,
        floor_type: this.floorTypeList
          .filter((f: any) => between(i, f.start_floor, f.end_floor))
          .map((f: any) => f.pk)[0],
        unit_code: 'unit_code', // Todo => 코드 부여 알고리즘 작성
      }))
      console.log({ project, unit_type, building_unit, bldg_line })
      console.log(floors)
    },
    ...mapActions('project', [
      'fetchTypeList',
      'fetchFloorTypeList',
      'fetchBuildingList',
      'fetchUnitList',
    ]),
  },
})
</script>
