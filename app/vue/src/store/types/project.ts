export interface Project {
  pk?: number
  company: number | null
  name: string
  order: number | null
  kind: string
  kind_desc?: string
  start_year: string
  is_direct_manage: boolean
  is_returned_area: boolean
  is_unit_set: boolean
  local_zipcode: string
  local_address1: string
  local_address2: string
  local_address3: string
  area_usage: string
  build_size: string
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
  sort: '' | '1' | '2' | '3' | '4' | '5' | '6'
  color: string
  actual_area: number | null
  supply_area: number | null
  contract_area: number | null
  average_price: number
  num_unit: number
}

export interface ProIncBudget {
  pk?: number
  project?: number
  account_d1: number
  account_d2: number
  order_group: number | null
  unit_type: number | null
  item_name: string
  average_price: number | null
  quantity: number
  budget: number
}

export interface ProOutBudget {
  pk?: number
  project?: number
  account_d1: number
  account_d2: number
  item_name: string
  basis_calc: string
  budget: number
}

export interface StatusOutBudget {
  pk?: number
  project?: number
  order?: number
  account_d2: {
    name: string
    pro_d3s: Array<number>
  }
  account_d3: {
    pk: number
    name: string
    sub_title: string
  }
  account_opt: string
  item_name: string
  basis_calc: string
  budget: number
}

export interface ExecAmountToBudget {
  acc_d3: number
  all_sum: number
  month_sum: number
}

export interface UnitFloorType {
  pk: number
  project: number
  start_floor: number
  end_floor: number
  extra_cond: string
  alias_name: string
}

export interface BuildingUnit {
  pk: number
  project: number
  name: string
}

export interface KeyUnit {
  pk: number
  contract: Contract | null
}

interface Contract {
  pk: number
  contractor: {
    status: string
    name: string
  }
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

export interface AllSite {
  pk: number
  __str__: string
}

export interface AllOwner {
  pk: number
  owner: string
}

export interface Site {
  pk: number | null
  project: number | null
  order: number | null
  district: string
  lot_number: string
  site_purpose: string
  official_area: string
  returned_area: number | null
  rights_restrictions: string
  dup_issue_date: string | null
  owners?: SimpleOwner[]
}

type OwnSort = '개인' | '법인' | '국공유지'

interface SimpleOwner {
  pk: number
  owner: string
  own_sort_desc: OwnSort
}

export interface SiteOwner {
  pk: number | null
  project: number | null
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
  sites: SimpleSite[]
  counsel_record: string
}

export interface SimpleSite {
  pk: number
  site: number
  __str__: string
  ownership_ratio: string
  owned_area: string
  acquisition_date: string | null
}

export interface Relation {
  pk: number | null
  site: number | null
  site_owner: number | null
  ownership_ratio: string
  owned_area: string
  acquisition_date: null | string
}

export interface SiteContract {
  pk: number | null
  project: number | null
  owner: number | null
  owner_desc?: SimpleOwner
  contract_date: string | null
  total_price: number | null
  contract_area: number | null
  down_pay1: number | null
  down_pay1_is_paid: boolean
  down_pay2: number | null
  down_pay2_is_paid: boolean
  inter_pay1: number | null
  inter_pay1_date: string | null
  inter_pay1_is_paid: boolean
  inter_pay2: number | null
  inter_pay2_date: string | null
  inter_pay2_is_paid: boolean
  remain_pay: number | null
  remain_pay_date: string | null
  remain_pay_is_paid: boolean
  ownership_completion: boolean
  acc_bank: string
  acc_number: string
  acc_owner: string
  note: string
}
