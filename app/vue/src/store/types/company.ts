export interface Staff {
  pk?: number
  company?: string
  sort?: '1' | '2'
  sort_desc?: '임원' | '직원'
  name: string
  id_number: string
  personal_phone: string
  email: string
  department: string
  grade: string
  position: string
  duty: string
  date_join: string | null
  date_leave: string | null
  status: '1' | '2' | '3' | '4'
  status_desc?: '근무 중' | '휴직 중' | '퇴직신청' | '퇴사처리'
}

export type StaffFilter = {
  page?: number
  com?: number
  sort?: '1' | '2'
  dep?: string
  gra?: string
  pos?: string
  dut?: string
  sts?: string
  q?: string
}

export interface Department {
  pk?: number
  company?: string
  upper_depart: number | null
  level: number
  name: string
  task: string
  staffs?: []
}

export type DepFilter = {
  page?: number
  com?: number
  upp?: string
  q?: string
}

export interface Grade {
  pk?: number
  company?: string
  grade: string
  promotion_period: number
  criteria_new: string
}

export interface Position {
  pk?: number
  company?: string
  level: number
  position: string
}

export type PosFilter = {
  page?: number
  com?: number
  q?: string
}

export interface DutyTitle {
  pk?: number
  company?: string
  title: string
}

export type ComFilter = {
  page?: number
  com?: number
  q?: string
}
