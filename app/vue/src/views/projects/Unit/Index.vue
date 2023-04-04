<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { CreateUnit, useProjectData } from '@/store/pinia/project_data'
import { message } from '@/utils/helper'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UnitController from '@/views/projects/Unit/components/UnitController.vue'
import UnitTable from '@/views/projects/Unit/components/UnitTable.vue'

const alertModal = ref()

const bldgName = ref('')

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const proDataStore = useProjectData()
const numUnitByType = computed(() => proDataStore.numUnitByType)
const simpleUnits = computed(() => proDataStore.simpleUnits)

const fetchTypeList = (projId: number) => proDataStore.fetchTypeList(projId)
const fetchFloorTypeList = (projId: number) =>
  proDataStore.fetchFloorTypeList(projId)
const fetchBuildingList = (projId: number) =>
  proDataStore.fetchBuildingList(projId)
const fetchHouseUnitList = (projId: number, bldg?: number) =>
  proDataStore.fetchHouseUnitList(projId, bldg)

const createUnit = (payload: CreateUnit) => proDataStore.createUnit(payload)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchTypeList(target)
    fetchFloorTypeList(target)
    fetchBuildingList(target)
  } else {
    proDataStore.unitTypeList = []
    proDataStore.floorTypeList = []
    proDataStore.buildingList = []
  }
  proDataStore.houseUnitList = []
}

const bldgSelect = (bldg: { pk: number; name: string }) => {
  if (!!bldg.pk) fetchHouseUnitList(project.value, bldg.pk)
  else proDataStore.houseUnitList = []
  bldgName.value = bldg.name
}

type OriginalUnit = {
  type: number
  building: number
  line: number
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

onBeforeMount(() => {
  fetchTypeList(project.value)
  fetchFloorTypeList(project.value)
  fetchBuildingList(project.value)
  proDataStore.houseUnitList = []
})
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
      <UnitTable :bldg-name="bldgName" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>

  <AlertModal ref="alertModal" />
</template>
