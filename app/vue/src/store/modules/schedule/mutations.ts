import { ScheduleState, Schedule } from '@/store/modules/schedule/state'

const mutations = {
  updateState: (
    state: ScheduleState,
    payload: { [key: string]: null | Schedule | Schedule[] },
  ) => {
    Object.keys(payload).forEach(key => {
      if (state.hasOwnProperty(key)) state[key] = payload[key]
    })
  },
}

export default mutations
