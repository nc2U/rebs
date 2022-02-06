import { Company, CompanyState } from '@/store/modules/settings/state'

const getters = {
  comSelect(state: CompanyState) {
    const comList = state.companyList.map((com: Company) => ({
      value: com.pk,
      text: com.name,
    }))
    return comList
  },
}

export default getters
