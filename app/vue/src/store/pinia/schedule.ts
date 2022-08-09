import api from '@/api'
import { computed, ref, reactive, Ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
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

export interface Event {
  title: string
  allDay: boolean
  start: string
  end: string
}

const transform = (payload: Event) => {
  const { title, start, allDay, end } = payload

  return {
    title: title,
    all_day: allDay,
    start_date: allDay ? start : null,
    end_date: allDay ? end : null,
    start_time: !allDay ? start : null,
    end_time: !allDay ? end : null,
  }
}

export const useScheduleStore = defineStore('schedule', () => {
  const schedule: Ref<Schedule> | Ref<null> = ref(null)
  const scheduleList: Schedule[] = reactive([])

  const events = computed(() => {
    return scheduleList.map((s: Schedule) => ({
      id: s.pk.toString(),
      title: s.title,
      start: s.all_day ? s.start_date : s.start_time,
      end: s.all_day ? s.end_date : s.end_time,
    }))
  })

  const fetchScheduleList = (month?: string) => {
    const mon = month ? month : new Date().toISOString().slice(0, 7)
    api
      .get(`/schedule/?search=${mon}`)
      .then(res =>
        scheduleList.splice(0, scheduleList.length, ...res.data.results),
      )
      .catch(err => errorHandle(err.response))
  }

  const createSchedule = (payload: Event) => {
    const eventData = transform(payload)
    api
      .post('/schedule/', eventData)
      .then(() => {
        fetchScheduleList(payload.start.substr(0, 7))
        message()
      })
      .catch(err => errorHandle(err.response))
  }

  const fetchSchedule = (pk: number) => {
    api
      .get(`/schedule/${pk}/`)
      .then(res => (schedule.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }

  const updateSchedule = (payload: { pk: string; data: Event }) => {
    const { pk, data } = payload
    const eventData = transform(data)
    console.log(pk, eventData)
    api
      .put(`/schedule/${pk}/`, eventData)
      .then(res => {
        fetchSchedule(res.data.pk)
        fetchScheduleList()
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteSchedule = (pk: string) => {
    api
      .delete(`/schedule/${pk}`)
      .then(() => {
        fetchScheduleList()
        message('danger', '알림!', '삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  }

  return {
    schedule,
    scheduleList,
    events,
    fetchScheduleList,
    createSchedule,
    fetchSchedule,
    updateSchedule,
    deleteSchedule,
  }
})
