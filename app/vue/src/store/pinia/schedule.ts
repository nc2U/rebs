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

  const createSchedule = (payload: any) => {
    api
      .post('/schedule/', payload)
      .then(() => {
        fetchScheduleList()
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const fetchSchedule = (pk: number) => {
    api
      .get(`/schedule/${pk}/`)
      .then(res => (schedule.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }

  const patchSchedule = ({ pk, data }: { pk: number; data: Schedule }) => {
    api
      .patch(`/schedule/${pk}`, data)
      .then(res => {
        fetchSchedule(res.data.pk)
        fetchScheduleList()
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const updateSchedule = ({ pk, data }: { pk: number; data: Schedule }) => {
    api
      .put(`/schedule/${pk}`, data)
      .then(res => {
        fetchSchedule(res.data.pk)
        fetchScheduleList()
        message()
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deleteSchedule = (pk: number) => {
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
    patchSchedule,
    updateSchedule,
    deleteSchedule,
  }
})
