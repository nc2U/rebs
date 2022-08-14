import { State } from '@/store'
import { Company } from '@/store/pinia/company'

export interface CompanyState extends State {
  companyList: Company[]
  company: Company | null
}

const state: CompanyState = {
  companyList: [],
  company: null,
}

export default state
