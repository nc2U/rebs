export interface Price {
  pk: number
  project: number
  order_group: number
  unit_type: number
  unit_floor_type: number
  price_build: number
  price_land: number
  price_tax: number
  price: number
}

export interface PayOrder {
  pk: number
  project: number
  pay_sort: string
  pay_code: number
  pay_time: number
  pay_name: string
  alias_name: string
  is_pm_cost: boolean
  pay_due_date: Date
  extra_due_date: Date
}

export interface CashState {
  priceList: Price[]
  price: Price | null
  payOrderList: PayOrder[]
}

const state: CashState = {
  priceList: [],
  price: null,
  payOrderList: [],
}

export default state
