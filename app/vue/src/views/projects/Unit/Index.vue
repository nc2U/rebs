<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UnitController from '@/views/projects/Unit/components/UnitController.vue'
import UnitListTable from '@/views/projects/Unit/components/UnitListTable.vue'
import { message } from '@/utils/helper'

const bldgName = ref('')

const store = useStore()
const projectStore = useProject()

const project = computed(() => projectStore.project?.pk)
const numUnitByType = computed(() => store.state.project.numUnitByType)
const simpleUnits = computed(() => store.getters['project/simpleUnits'])
const initProjId = computed(() => projectStore.initProjId)

const fetchTypeList = (projId: number) =>
  store.dispatch('project/fetchTypeList', projId)
const fetchFloorTypeList = (projId: number) =>
  store.dispatch('project/fetchFloorTypeList', projId)
const fetchBuildingList = (projId: number) =>
  store.dispatch('project/fetchBuildingList', projId)
const fetchHouseUnitList = (payload: any) =>
  store.dispatch('project/fetchHouseUnitList', payload)
const createUnit = (payload: any) =>
  store.dispatch('project/createUnit', payload)

onBeforeMount(() => {
  fetchTypeList(initProjId.value)
  fetchFloorTypeList(initProjId.value)
  fetchBuildingList(initProjId.value)
  store.commit('project/updateState', { houseUnitList: [] })
})
const onSelectAdd = (target: any) => {
  if (target !== '') {
    fetchTypeList(target)
    fetchFloorTypeList(target)
    fetchBuildingList(target)
  } else {
    store.commit('project/updateState', {
      unitTypeList: [],
      floorTypeList: [],
      buildingList: [],
    })
  }
  store.commit('project/updateState', { houseUnitList: [] })
}
const bldgSelect = (bldg: any) => {
  if (bldg.pk !== '')
    fetchHouseUnitList({ project: project.value, bldg: bldg.pk })
  else store.commit('project/updateState', { houseUnitList: [] })
  bldgName.value = bldg.name
}

const unitRegister = (payload: any) => {
  const unit_type = Number(payload.type)
  const building_unit = Number(payload.building)
  const bldg_line = payload.line
  const midWord = bldg_line < 10 ? '0' : ''
  const size = payload.maxFloor - payload.minFloor + 1
  const range = (size: number, min: number): number[] =>
    [...Array(size).keys()].map(key => key + min)
  const between = (x: number, min: number, max: number): boolean =>
    x >= min && x <= max
  const getCode = (num: number, digit: number) => {
    const prefix = '0'.repeat(digit - `${num}`.length)
    const typeStr = payload.typeName.replace(/[^0-9a-zA-Z]/g, '')
    const typeDigit = payload.maxLength - typeStr.length
    const suffix = typeDigit >= 1 ? '0'.repeat(typeDigit - 1) + '1' : ''
    return `${typeStr}${suffix}${prefix}${num}`
  }
  let num = numUnitByType.value

  const isExist = range(size, payload.minFloor).map(i =>
    simpleUnits.value
      .filter((u: any) => u.line === bldg_line)
      .map((u: any) => u.floor)
      .includes(i),
  )

  if (isExist.includes(true)) {
    alert('해당 범위의 호수 중 이미 등록되어 있는 유니트가 있습니다.')
    return
  } else {
    const inputUnits = range(size, payload.minFloor).map(i => ({
      floor_no: i,
      name: `${i}${midWord}${bldg_line}`,
      floor_type: payload.floors
        .filter((f: any) => between(i, f.start, f.end))
        .map((f: any) => f.pk)[0],
      unit_code: getCode((num += 1), `${payload.maxUnits}`.length),
    }))

    inputUnits.forEach(unit => {
      createUnit({
        ...{ project: project.value, unit_type, building_unit, bldg_line },
        ...unit,
      })
    })
    fetchHouseUnitList({ project: project.value, bldg: building_unit })
    message()
  }
}
</script>

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
