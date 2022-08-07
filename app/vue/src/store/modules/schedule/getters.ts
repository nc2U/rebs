import { ScheduleState, Schedule } from '@/store/modules/schedule/state'

const getters = {
  events: (state: ScheduleState) => {
    return state.scheduleList.map((s: Schedule) => ({
      id: s.pk.toString(),
      title: s.title,
      start: s.all_day ? s.start_date : s.start_time,
      end: s.all_day ? s.end_date : s.end_time,
    }))
  },
}

export default getters
