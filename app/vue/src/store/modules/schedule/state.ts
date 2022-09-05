import { State } from '@/store'
import { Schedule } from '@/store/types/schedule'

export interface ScheduleState extends State {
  scheduleList: Schedule[]
  schedule: Schedule | null
}

const state: ScheduleState = {
  scheduleList: [],
  schedule: null,
}

export default state
