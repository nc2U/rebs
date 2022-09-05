import { State } from '@/store'
import { Company } from '@/store/types/settings'

export interface CompanyState extends State {
  companyList: Company[]
  company: Company | null
}

const state: CompanyState = {
  companyList: [],
  company: null,
}

export default state
