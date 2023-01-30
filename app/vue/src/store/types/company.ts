export interface Department {
  pk?: number
  company?: string
  upper_depart: number | null
  level: number
  name: string
  task: string
  staffs?: []
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

export interface Staff {
  pk?: number
  company?: string
  department?: string
  rank?: string
  name: string
  birth_date: string | null
  gender: 'M' | 'F'
  gender_desc?: '남성' | '여성'
  entered_date: string | null
  personal_phone: string
  email: string
  status: '1' | '2' | '3' | '4'
  status_desc?: '근무 중' | '정직 중' | '퇴사신청' | '퇴사처리'
}
