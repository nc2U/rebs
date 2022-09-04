import { State } from '@/store'
import {
  Project,
  UnitType,
  UnitFloorType,
  BuildingUnit,
  HouseUnit,
  ProjectBudget,
  Site,
  SiteOwner,
  Relation,
  SiteContract,
} from '@/store/types/project'

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
  siteOwnerRelationList: Relation[]
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
