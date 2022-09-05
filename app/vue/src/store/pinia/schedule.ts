import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
import { Schedule, Event } from '@/store/types/schedule'

const transform = (payload: Event) => {
  const { title, start, allDay, end } = payload

  return {
    title,
    all_day: allDay,
    start_date: allDay ? start : null,
    end_date: allDay ? end : null,
    start_time: allDay ? null : start,
    end_time: allDay ? null : end,
  }
}

export const useSchedule = defineStore('schedule', () => {
  // states
  const schedule = ref<Schedule | null>(null)
  const scheduleList = ref<Schedule[]>([])

  // getters
  const events = computed(() => {
    return scheduleList.value.map((s: Schedule) => ({
      id: s.pk.toString(),
      title: s.title,
      start: s.all_day ? s.start_date : s.start_time,
      end: s.all_day ? s.end_date : s.end_time,
    }))
  })

  // actions
  const fetchScheduleList = (month?: string) => {
    const mon = month ? month : new Date().toISOString().slice(0, 7)
    api
      .get(`/schedule/?search=${mon}`)
      .then(res => (scheduleList.value = res.data.results))
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
