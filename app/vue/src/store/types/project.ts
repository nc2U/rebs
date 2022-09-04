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

export interface AllSite {
  pk: number
  __str__: string
}

export interface AllOwner {
  pk: number
  owner: string
}

export interface Site {
  pk: number
  project: number
  order: number
  district: string
  lot_number: string
  site_purpose: string
  official_area: string
  returned_area: string | null
  rights_restrictions: string
  dup_issue_date: string
  owners: SimpleOwner[]
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
  sites: {
    pk: number
    site: number
    __str__: string
    ownership_ratio: string
    owned_area: string
    acquisition_date: string | null
  }[]
  counsel_record: string
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
  pk: number
  project: number
  owner: number
  owner_desc: SimpleOwner
  contract_date: string
  total_price: number
  contract_area: string | null
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
  remain_pay: number
  remain_pay_date: string | null
  remain_pay_is_paid: boolean
  ownership_completion: boolean
  acc_bank: string
  acc_number: string
  acc_owner: string
  note: string
}
