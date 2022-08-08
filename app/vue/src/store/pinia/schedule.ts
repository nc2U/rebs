import api from '@/api'
import { computed, ref, reactive, Ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle } from '@/utils/helper'
import Schedule from '@/store/modules/schedule'

interface Schedule {
  pk: number
  title: string
  all_day: boolean
  start_date: string | null
  end_date: string | null
  start_time: string | null
  end_time: string | null
}

export const useScheduleListStore = defineStore('scheduleList', () => {
  const scheduleList: Schedule[] = reactive([])

  const events = computed(() => {
    return scheduleList.map((s: Schedule) => ({
      id: s.pk.toString(),
      title: s.title,
      start: s.all_day ? s.start_date : s.start_time,
      end: s.all_day ? s.end_date : s.end_time,
    }))
  })

  const fetchScheduleList = () => {
    api
      .get('/schedule/')
      .then(res =>
        scheduleList.splice(0, scheduleList.length, ...res.data.results),
      )
      .catch(err => errorHandle(err.response))
  }

  return {
    scheduleList,
    events,
    fetchScheduleList,
  }
})

export const useScheduleStore = defineStore('schedule', () => {
  const schedule: Ref<Schedule> | Ref<null> = ref(null)

  return {
    schedule,
  }
})
