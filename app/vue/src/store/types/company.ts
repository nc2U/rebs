export interface Staff {
  pk?: number
  company?: string
  name: string
  id_number: string
  personal_phone: string
  email: string
  department: string
  rank: string
  entered_date: string | null
  status: '1' | '2' | '3' | '4'
  status_desc?: '근무 중' | '휴직 중' | '퇴사신청' | '퇴사처리'
}

export type StaffFilter = {
  page?: number
  com?: number
  dep?: string
  rank?: string
  sts?: string
  q?: string
}

export interface Rank {
  pk?: number
  company?: string
  sort?: '1' | '2'
  sort_desc?: '임원' | '직원'
  level: number | null
  rank: string
  title: string
  description: string
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
