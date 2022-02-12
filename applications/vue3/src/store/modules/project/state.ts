import { Company } from '@/store/modules/settings/state'
import { Contract } from '@/store/modules/contract/state'
import {
  ProjectAccountD1,
  ProjectAccountD2,
} from '@/store/modules/project_cash/state'
import { User } from '@/store/modules/accounts/state'

export interface Project {
  pk: number
  company: Company
  name: string
  order: number | null
  kind: string
  kind_desc: string
  start_year: string
  is_direct_manage: boolean
  is_returned_area: boolean
  is_unit_set: boolean
  local_zipcode: string | null
  local_address1: string | null
  local_address2: string | null
  local_address3: string | null
  area_usage: string | null
  build_size: string | null
  num_unit: number | null
  buy_land_extent: number | null
  scheme_land_extent: number | null
  donation_land_extent: number | null
  on_floor_area: number | null
  under_floor_area: number | null
  total_floor_area: number | null
  build_area: number | null
  floor_area_ratio: number | null
  build_to_land_ratio: number | null
  num_legal_parking: number | null
  num_planed_parking: number | null
}

export interface UnitType {
  project: Project
  name: string
  color: string
  average_price: number
  num_unit: number
}

export interface UnitFloorType {
  project: Project
  start_floor: number
  end_floor: number
  alias_name: string
}

export interface ContractUnit {
  project: Project
  unit_type: UnitType
  unit_code: string
  contract: Contract
}

export interface UnitNumber {
  project: Project
  unit_type: UnitType
  floor_type: UnitFloorType
  bldg_no: string
  bldg_unit_no: string
  contract_unit: ContractUnit
  bldg_line: number
  floor_no: number
  is_hold: boolean
  hold_reason: string
}

export interface ProjectBudget {
  project: Project
  account_d1: ProjectAccountD1
  account_d2: ProjectAccountD2
  budget: number
}

export interface Site {
  pk: number
  project: Project
  order: number
  district: string
  lot_number: string
  site_purpose: string
  official_area: number
  returned_area: number
  rights_restrictions: string
  dup_issue_date: Date
  created_at: Date
  updated_at: Date
}

export interface SiteOwner {
  owner: string
  date_of_birth: Date
  phone1: string
  phone2: string
  zipcode: string
  address1: string
  address2: string
  address3: string
  own_sort: string
  own_sort_desc: string
  sites: Site[]
  counsel_record: string
  user: User
  created_at: Date
  updated_at: Date
}

export interface SiteOwnshipRelationship {
  site: Site
  site_owner: SiteOwner
  ownership_ratio: number
  owned_area: number
  acquisition_date: Date
}

export interface SiteContract {
  project: Project
  owner: SiteOwner
  contract_date: Date
  total_price: number
  down_pay1: number
  down_pay1_is_paid: boolean
  down_pay2: number
  down_pay2_is_paid: boolean
  inter_pay1: number
  inter_pay1_date: Date
  inter_pay1_is_paid: boolean
  inter_pay2: number
  inter_pay2_date: Date
  inter_pay2_is_paid: boolean
  remain_pay: number
  remain_pay_date: Date
  remain_pay_is_paid: boolean
  ownership_completion: boolean
  acc_bank: string
  acc_number: string
  acc_owner: string
  note: string
  user: User
  created_at: Date
  updated_at: Date
}

export interface ProjectState {
  projectList: Project[]
  project: Project | null
  unitTypeList: UnitType[]
  floorTypeList: UnitFloorType[]
  contUnitList: ContractUnit[]
  cont_unit: ContractUnit | null
  unitNumberList: UnitNumber[]
  unit_number: UnitNumber | null
  projectBudgetList: ProjectBudget[]
  projectBudget: ProjectBudget | null
  siteList: Site[]
  site: Site | null
  siteOwnerList: SiteOwner[]
  site_owner: SiteOwner | null
  siteOwnerRelationList: SiteOwnshipRelationship[]
  site_owner_relation: SiteOwnshipRelationship | null
  siteContractList: SiteContract[]
  site_contract: SiteContract | null
}

const state: ProjectState = {
  projectList: [],
  project: null,
  unitTypeList: [],
  floorTypeList: [],
  contUnitList: [],
  cont_unit: null,
  unitNumberList: [],
  unit_number: null,
  projectBudgetList: [],
  projectBudget: null,
  siteList: [],
  site: null,
  siteOwnerList: [],
  site_owner: null,
  siteOwnerRelationList: [],
  site_owner_relation: null,
  siteContractList: [],
  site_contract: null,
}

export default state
