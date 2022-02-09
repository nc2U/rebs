interface Price {
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

export interface CashState {
  priceList: Price[]
}

const state: CashState = {
  priceList: [],
}

export default state
