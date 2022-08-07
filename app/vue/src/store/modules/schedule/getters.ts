import { ScheduleState, Schedule } from '@/store/modules/schedule/state'

const getters = {
  events: (state: ScheduleState) => {
    return state.scheduleList.map((s: Schedule) => ({
      id: s.pk.toString(),
      title: s.title,
      start: s.start_time || s.event_date,
    }))
  },
}

export default getters
