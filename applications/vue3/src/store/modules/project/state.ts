export interface Project {
  pk: number
  company: number
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

export interface UnitFloorType {
  pk: number
  project: number
  start_floor: number
  end_floor: number
  extra_cond: string
  alias_name: string
}

export interface BuildingNumber {
  pk: number
  project: number
  name: string
}

export interface ContractUnit {
  pk: number
  project: number
  unit_type: number
  unit_code: string
  contract: number
}

export interface UnitNumber {
  pk: number
  project: number
  unit_type: number
  floor_type: number
  building_number: string
  bldg_unit_no: string
  contract_unit: number
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

export interface Site {
  pk: number
  project: number
  order: number
  district: string
  lot_number: string
  site_purpose: string
  official_area: number
  returned_area: number
  rights_restrictions: string
  dup_issue_date: string
  created_at: string
  updated_at: string
}

export interface SiteOwner {
  pk: number
  owner: string
  date_of_birth: string | null
  phone1: string
  phone2: string
  zipcode: string
  address1: string
  address2: string
  address3: string
  own_sort: string
  own_sort_desc: string
  sites: number[]
  counsel_record: string
  user: number
}

export interface SiteOwnshipRelationship {
  pk: number
  site: number
  site_owner: number
  ownership_ratio: number | null
  owned_area: number | null
  acquisition_date: string | null
}

export interface SiteContract {
  pk: number
  project: number
  owner: number
  contract_date: string
  total_price: number
  down_pay1: number
  down_pay1_is_paid: boolean
  down_pay2: number
  down_pay2_is_paid: boolean
  inter_pay1: number
  inter_pay1_date: string | null
  inter_pay1_is_paid: boolean
  inter_pay2: number
  inter_pay2_date: string | null
  inter_pay2_is_paid: boolean
  remain_pay: number
  remain_pay_date: string | null
  remain_pay_is_paid: boolean
  ownership_completion: boolean
  acc_bank: string
  acc_number: string
  acc_owner: string
  note: string
}

export interface ProjectState {
  projectList: Project[]
  project: Project | null
  unitTypeList: UnitType[]
  floorTypeList: UnitFloorType[]
  buildingList: BuildingNumber[]
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
  buildingList: [],
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
