import { State } from '@/store'
import {
  Project,
  ProjectBudget,
  UnitType,
  UnitFloorType,
  BuildingUnit,
  HouseUnit,
  Site,
  SiteOwner,
  Relation,
  SiteContract,
} from '@/store/types/project'

export interface ProjectState extends State {
  projectList: Project[]
  project: Project | null
  projectBudgetList: ProjectBudget[]

  unitTypeList: UnitType[]
  floorTypeList: UnitFloorType[]
  buildingList: BuildingUnit[]
  houseUnitList: HouseUnit[]
  houseUnitNum: number
  numUnitByType: number

  siteList: Site[]
  siteOwnerList: SiteOwner[]
  siteOwnerRelationList: Relation[]
  siteContractList: SiteContract[]
}

const state: ProjectState = {
  projectList: [],
  project: null,
  projectBudgetList: [],

  unitTypeList: [],
  floorTypeList: [],
  buildingList: [],
  houseUnitList: [],
  houseUnitNum: 0,
  numUnitByType: 0,

  siteList: [],
  siteOwnerList: [],
  siteOwnerRelationList: [],
  siteContractList: [],
}

export default state
