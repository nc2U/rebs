import { State } from '@/store'

export interface Schedule {
  name: string
  task: string
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
