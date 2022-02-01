import { User } from '@/store/modules/accounts/state'
import { Project } from '@/store/modules/project/state'

export interface Contract {
  id: number
  project: Project
  order_group: OrderGroup
  serial_number: string
  activation: boolean
  created_at: Date
  updted_at: Date
  user: User
}

export interface OrderGroup {
  id: number
  project: Project
  order_number: number
  sort: string
  sort_desc: string
  order_group_name: string
}

export interface ContractState {
  contractList: Contract[]
  contract: Contract | null
  orderGroupList: OrderGroup[]
  order_group: OrderGroup | null
}

const state = {
  contractList: [],
  contract: null,
  orderGroupList: [],
  order_group: null,
}

export default state
