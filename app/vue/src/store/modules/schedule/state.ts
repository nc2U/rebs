import { State } from '@/store'

export interface Schedule {
  pk: number
  title: string
  all_day: boolean
  start_date: string | null
  end_date: string | null
  start_time: string | null
  end_time: string | null
}

export interface ScheduleState extends State {
  scheduleList: Schedule[]
  schedule: Schedule | null
}

const state: ScheduleState = {
  scheduleList: [],
  schedule: null,
}

export default state
