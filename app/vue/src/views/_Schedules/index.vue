<script lang="ts" setup>
import '@fullcalendar/core/vdom' // solve problem with Vite
import FullCalendar, {
  CalendarOptions,
  Identity,
  EventSourceInput,
  DateSelectArg,
  EventClickArg,
} from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

import { computed, onBeforeMount, reactive, watch } from 'vue'
import { useScheduleListStore } from '@/store/pinia/schedule'
import CalendarInfo from './components/CalendarInfo.vue'

const scheduleList = useScheduleListStore()

const currentEvents = computed(() => scheduleList.events)

const fetchScheduleList = () => scheduleList.fetchScheduleList()

watch(currentEvents, () => calendarOptions.initialEvents)

const handleDateSelect = (selectInfo: DateSelectArg) => {
  // alert('날짜 클릭 시 이벤트')
  let title = prompt('Please enter a new title for your event')
  let calendarApi = selectInfo.view.calendar
  calendarApi.unselect() // clear date selection

  if (title) {
    calendarApi.addEvent({
      // id: createEventId(),
      title,
      start: selectInfo.startStr,
      end: selectInfo.endStr,
      allDay: selectInfo.allDay,
    })
  }
}

const handleEventClick = (clickInfo: EventClickArg) => {
  // 일정 클릭 시 이벤트
  if (
    confirm(
      `Are you sure you want to delete the event '${clickInfo.event.title}'`,
    )
  ) {
    clickInfo.event.remove()
  }
}

const calendarOptions = reactive({
  plugins: [
    dayGridPlugin,
    timeGridPlugin,
    interactionPlugin, // needed for dateClick
  ],
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay',
  },
  initialView: 'dayGridMonth',
  events: currentEvents,
  // initialEvents: currentEvents, // alternatively, use the `events` setting to fetch from a feed
  editable: true,
  selectable: true,
  selectMirror: true,
  dayMaxEvents: true,

  weekends: true,

  select: handleDateSelect,
  eventClick: handleEventClick,
  // eventsSet: handleEvents,

  // you can update a remote database when these fire:
  eventAdd: () => alert('add'),
  eventChange: () => alert('change'),
  eventRemove: () => alert('del'),
})

const handleWeekendsToggle = () => {
  calendarOptions.weekends = !calendarOptions.weekends // update a property
}

onBeforeMount(() => {
  fetchScheduleList()
})
</script>

<template>
  <div class="demo-app">
    <CRow>
      <CCol md="9">
        <CCard>
          <CCardHeader class="text-body">
            <CIcon name="cil-calendar" />
            Calendar
            <CBadge color="primary">Rebs</CBadge>
          </CCardHeader>
          <CCardBody>
            <div class="demo-app text-body">
              <div class="demo-app-main">
                <FullCalendar
                  class="demo-app-calendar"
                  :options="calendarOptions"
                >
                  <template #eventContent="arg">
                    <b>{{ arg.timeText }}</b>
                    <i>{{ arg.event.title }}</i>
                  </template>
                </FullCalendar>
              </div>
            </div>
          </CCardBody>
        </CCard>
      </CCol>

      <CalendarInfo
        :calendar-options="calendarOptions"
        :current-events="currentEvents"
        @weekends-toggle="handleWeekendsToggle"
      />
    </CRow>
  </div>
</template>
