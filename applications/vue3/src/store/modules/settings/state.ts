export interface Department {
  name: string
  task: string
}

interface Positions {
  id: number
  rank: string
  title: string
  description: string
}

export interface Company {
  id: number
  name: string
  ceo: string
  tax_number: string
  org_number: string
  business_cond: string
  business_even: string
  es_date: string
  op_date: string
  zipcode: string
  address1: string
  address2: string
  address3: string
  departments: Department[]
  positions: Positions[]
}

export interface CompanyState {
  companyList: Company[]
  company: Company | null
}

const state: CompanyState = {
  companyList: [],
  company: null,
}

export default state
