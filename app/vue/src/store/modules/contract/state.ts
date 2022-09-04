import { State } from '@/store'
import {
  Contract,
  Contractor,
  SubsSummary,
  ContractSummary,
  OrderGroup,
  KeyUnit,
  HouseUnit,
  SalesPrice,
  DownPayment,
  ContractRelease,
} from '@/store/types/contract'

export interface ContractState extends State {
  contractList: Contract[]
  contractsCount: number
  contract: Contract | null
  contractorList: Contractor[]
  contractor: Contractor | null
  subsSummaryList: SubsSummary[]
  contSummaryList: ContractSummary[]
  orderGroupList: OrderGroup[]
  keyUnitList: KeyUnit[]
  houseUnitList: HouseUnit[]
  salesPriceList: SalesPrice[]
  downPaymentList: DownPayment[]
  contReleaseList: ContractRelease[]
  contReleaseCount: number
  contRelease: ContractRelease | null
}

const state = {
  contractList: [],
  contractsCount: 0,
  contract: null,
  contractorList: [],
  contractor: null,
  subsSummaryList: [],
  contSummaryList: [],
  orderGroupList: [],
  keyUnitList: [],
  houseUnitList: [],
  salesPriceList: [],
  downPaymentList: [],
  contReleaseList: [],
  contReleaseCount: 0,
  contRelease: null,
}

export default state
