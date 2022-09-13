<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { CreateUnit, useProjectData } from '@/store/pinia/project_data'
import { message } from '@/utils/helper'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UnitController from '@/views/projects/Unit/components/UnitController.vue'
import UnitListTable from '@/views/projects/Unit/components/UnitListTable.vue'

const alertModal = ref()

const bldgName = ref('')

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const projectDataStore = useProjectData()
const numUnitByType = computed(() => projectDataStore.numUnitByType)
const simpleUnits = computed(() => projectDataStore.simpleUnits)

const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)
const fetchFloorTypeList = (projId: number) =>
  projectDataStore.fetchFloorTypeList(projId)
const fetchBuildingList = (projId: number) =>
  projectDataStore.fetchBuildingList(projId)
const fetchHouseUnitList = (projId: number, bldg?: number) =>
  projectDataStore.fetchHouseUnitList(projId, bldg)

const createUnit = (payload: CreateUnit) => projectDataStore.createUnit(payload)

onBeforeMount(() => {
  fetchTypeList(initProjId.value)
  fetchFloorTypeList(initProjId.value)
  fetchBuildingList(initProjId.value)
  projectDataStore.houseUnitList = []
})

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchTypeList(target)
    fetchFloorTypeList(target)
    fetchBuildingList(target)
  } else {
    projectDataStore.unitTypeList = []
    projectDataStore.floorTypeList = []
    projectDataStore.buildingList = []
  }
  projectDataStore.houseUnitList = []
}

const bldgSelect = (bldg: { pk: number; name: string }) => {
  if (!!bldg.pk) fetchHouseUnitList(project.value, bldg.pk)
  else projectDataStore.houseUnitList = []
  bldgName.value = bldg.name
}

type OriginalUnit = {
  building: number
  line: number
  type: number
  minFloor: number
  maxFloor: number
  typeName: string
  maxLength: number
  maxUnits: number
  floors: {
    pk: number
    start: number
    end: number
    name: string
  }[]
}

const unitRegister = (payload: OriginalUnit) => {
  const unit_type = payload.type
  const building_unit = payload.building
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
      .filter((u: { line: number }) => u.line === bldg_line)
      .map((u: { floor: number }) => u.floor)
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
        .filter((f: { start: number; end: number }) =>
          between(i, f.start, f.end),
        )
        .map((f: { pk: number }) => f.pk)[0],
      unit_code: getCode((num += 1), `${payload.maxUnits}`.length),
    }))

    inputUnits.forEach(unit => {
      createUnit({
        ...{ project: project.value, unit_type, building_unit, bldg_line },
        ...unit,
      })
    })
    fetchHouseUnitList(project.value, building_unit)
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

  <AlertModal ref="alertModal" />
</template>
