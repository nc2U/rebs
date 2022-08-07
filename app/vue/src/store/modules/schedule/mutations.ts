import { ScheduleState, Schedule } from '@/store/modules/schedule/state'

export const UPDATE_STATE = 'UPDATE_STATE'

const mutations = {
  UPDATE_STATE: (
    state: ScheduleState,
    payload: { [key: string]: null | Schedule | Schedule[] },
  ) => {
    Object.keys(payload).forEach(key => {
      if (state.hasOwnProperty(key)) state[key] = payload[key]
    })
  },
}

export default mutations
