import { State } from '@/store'
import { Project } from '@/store/pinia/project'
import {
  Site,
  SiteOwner,
  SiteOwnshipRelationship,
  SiteContract,
} from '@/store/pinia/project_site'

interface UnitType {
  pk: number
  project: number
  name: string
  color: string
  actual_area: number | null
  supply_area: number | null
  contract_area: number | null
  average_price: number
  num_unit: number
}

interface UnitFloorType {
  pk: number
  project: number
  start_floor: number
  end_floor: number
  extra_cond: string
  alias_name: string
}

interface Contract {
  pk: number
  contractor: {
    status: string
    name: string
  }
}

export interface KeyUnit {
  pk: number
  contract: Contract | null
}

export interface BuildingUnit {
  pk: number
  project: number
  name: string
}

export interface HouseUnit {
  pk: number
  project: number
  unit_type: number
  floor_type: number
  __str__: string
  building_unit: number
  name: string
  key_unit: KeyUnit
  bldg_line: number
  floor_no: number
  is_hold: boolean
  hold_reason: string
}

export interface ProjectBudget {
  pk: number
  project: number
  account_d1: number
  account_d2: number
  budget: number
}

export interface ProjectState extends State {
  projectList: Project[]
  project: Project | null
  unitTypeList: UnitType[]
  floorTypeList: UnitFloorType[]
  buildingList: BuildingUnit[]
  houseUnitList: HouseUnit[]
  houseUnitNum: number
  numUnitByType: number
  projectBudgetList: ProjectBudget[]
  siteList: Site[]
  siteOwnerList: SiteOwner[]
  siteOwnerRelationList: SiteOwnshipRelationship[]
  siteContractList: SiteContract[]
}

const state: ProjectState = {
  projectList: [],
  project: null,
  unitTypeList: [],
  floorTypeList: [],
  buildingList: [],
  houseUnitList: [],
  houseUnitNum: 0,
  numUnitByType: 0,
  projectBudgetList: [],
  siteList: [],
  siteOwnerList: [],
  siteOwnerRelationList: [],
  siteContractList: [],
}

export default state
