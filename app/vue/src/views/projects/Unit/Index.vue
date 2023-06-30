<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { CreateUnit, useProjectData } from '@/store/pinia/project_data'
import { message } from '@/utils/helper'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UnitController from '@/views/projects/Unit/components/UnitController.vue'
import UnitTable from '@/views/projects/Unit/components/UnitTable.vue'
import { HouseUnit } from '@/store/types/project'

const alertModal = ref()

const bldgPk = ref<null | number>(null)
const bldgName = ref('')

const projStore = useProject()
const project = computed(() => projStore.project?.pk)
watch(project, val => {
  if (!!val) dataSet(val)
  else dataReset()
  pDataStore.houseUnitList = []
})

const pDataStore = useProjectData()
const numUnitByType = computed(() => pDataStore.numUnitByType)
const simpleUnits = computed(() => pDataStore.simpleUnits)

const fetchTypeList = (projId: number) => pDataStore.fetchTypeList(projId)
const fetchFloorTypeList = (projId: number) =>
  pDataStore.fetchFloorTypeList(projId)
const fetchBuildingList = (projId: number) =>
  pDataStore.fetchBuildingList(projId)
const fetchHouseUnitList = (projId: number, bldg?: number) =>
  pDataStore.fetchHouseUnitList(projId, bldg)

const createUnit = (payload: CreateUnit) => pDataStore.createUnit(payload)
const patchUnit = (payload: HouseUnit & { bldg: number }) =>
  pDataStore.patchUnit(payload)

const bldgSelect = (bldg: { pk: number; name: string }) => {
  if (!!bldg.pk && project.value) fetchHouseUnitList(project.value, bldg.pk)
  else pDataStore.houseUnitList = []
  bldgPk.value = bldg.pk
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
  if (!!project.value) {
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
          ...{
            project: Number(project.value),
            unit_type,
            building_unit,
            bldg_line,
          },
          ...unit,
        })
      })
      fetchHouseUnitList(project.value, building_unit)
      message()
    }
  }
}

const onUpdate = (payload: HouseUnit) =>
  !!bldgPk.value
    ? patchUnit({
        ...payload,
        ...{
          project: project.value || projStore.initProjId,
          bldg: bldgPk.value,
        },
      })
    : alert('동(건물)을 선택하세요!')

const onDelete = (pk: number) => alert('delete! -- ' + pk)

const dataSet = (pk: number) => {
  fetchTypeList(pk)
  fetchFloorTypeList(pk)
  fetchBuildingList(pk)
}

const dataReset = () => {
  pDataStore.unitTypeList = []
  pDataStore.floorTypeList = []
  pDataStore.buildingList = []
}

onBeforeMount(() => {
  dataSet(project.value || projStore.initProjId)
  pDataStore.houseUnitList = []
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <UnitController
        :project="project"
        @bldg-select="bldgSelect"
        @unit-register="unitRegister"
      />
      <UnitTable
        :bldg-name="bldgName"
        @on-update="onUpdate"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>

  <AlertModal ref="alertModal" />
</template>
