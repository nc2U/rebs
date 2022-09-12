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
  __str__: string
  pay_sort: string
  pay_code: number
  pay_time: number
  pay_ratio: string | null
  pay_name: string
  alias_name: string
  is_pm_cost: boolean
  pay_due_date: string
  extra_due_date: string
}

export interface DownPay {
  pk: number
  project: number
  order_group: number
  unit_type: number
  number_payments: number
  payment_amount: number
}

export interface PaySumByType {
  unit_type: number
  type_total: number
}

export interface ContractNum {
  unit_type: number
  num_cont: number
}
