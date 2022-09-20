<script lang="ts" setup>
import { computed, onBeforeMount, reactive, ref, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { useSchedule } from '@/store/pinia/schedule'
import { addDays, diffDate } from '@/utils/baseMixins'
import '@fullcalendar/core/vdom' // solve problem with Vite
import { EventApi } from '@fullcalendar/common'
import FullCalendar, { DateSelectArg, EventClickArg } from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import CalendarInfo from './components/CalendarInfo.vue'
import FormModal from '@/components/Modals/FormModal.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const cal = ref()
const month = ref('')
const scheduleStore = useSchedule()
const currentEvents = computed(() => scheduleStore.events)

const fetchScheduleList = (mon = '') => scheduleStore.fetchScheduleList(mon)

const mode = ref<'create' | 'update'>('create')

const formModal = ref()
const alertModal = ref()
const eventId = ref<string>('')
const eventTitle = ref('')

type CalEvent = {
  start: string
  end: string
  allDay: boolean
}

const newEvent = reactive<CalEvent>({
  start: '',
  end: '',
  allDay: true,
})

const accountStore = useAccount()
const handleDateSelect = (selectInfo: DateSelectArg) => {
  if (accountStore.staffAuth) {
    mode.value = 'create'
    eventTitle.value = ''
    formModal.value.callModal()
    let calendarApi = selectInfo.view.calendar
    calendarApi.unselect() // clear date selection
    newEvent.start = selectInfo.startStr
    newEvent.end = selectInfo.endStr
    newEvent.allDay = selectInfo.allDay
  } else
    alertModal.value.callModal(
      '',
      '스태프(일정 등록) 권한이 없습니다. 관리자에게 문의하여 주십시요.',
    )
}

const eventManagement = () => {
  const eventData = { title: eventTitle.value, ...newEvent }
  if (mode.value === 'create') scheduleStore.createSchedule(eventData)
  else if (mode.value === 'update')
    scheduleStore.updateSchedule({
      pk: eventId.value,
      ...{ data: eventData },
    })
  formModal.value.close()
}

const transformData = (event: EventApi) => {
  const title = event.title
  const allDay = event.allDay
  const s = event._instance?.range.start
    .toISOString()
    .replace('.000Z', '+09:00')
  const e = event._instance?.range.end.toISOString().replace('.000Z', '+09:00')
  const start = allDay ? s?.substr(0, 10) : s
  const end = allDay ? e?.substr(0, 10) : e
  return { title, allDay, start, end }
}

const handleChange = (el: EventClickArg) => {
  const pk = el.event.id
  const eventDate = transformData(el.event)
  scheduleStore.updateSchedule({ pk, data: eventDate })
}

const confirmModal = ref()
const handleEventClick = (clickInfo: EventClickArg) => {
  if (accountStore.staffAuth) {
    mode.value = 'update'
    eventId.value = clickInfo.event.id
    eventTitle.value = clickInfo.event.title
    newEvent.start = clickInfo.event.startStr
    newEvent.end = clickInfo.event.endStr
    newEvent.allDay = clickInfo.event.allDay
    formModal.value.callModal()
  } else
    alertModal.value.callModal(
      '',
      '스태프(일정 수정) 권한이 없습니다. 관리자에게 문의하여 주십시요.',
    )
}

const removeConfirm = () => {
  formModal.value.visible = false
  confirmModal.value.callModal()
}

const eventRemove = () => {
  scheduleStore.deleteSchedule(eventId.value)
  confirmModal.value.close()
}

const handleMonthChange = (payload: CalEvent) => {
  const diff = diffDate(payload.start, new Date(payload.end))
  const addDay = diff > 10 ? 7 : 1
  const date = new Date(addDays(new Date(payload.start), addDay))
  month.value = date.toISOString().substr(0, 7)
}

watch(month, val => fetchScheduleList(val))

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
  editable: true,
  selectable: true,
  selectMirror: true,
  dayMaxEvents: true,

  weekends: true,

  select: handleDateSelect,
  eventClick: handleEventClick,
  datesSet: handleMonthChange, // prev, next button click event

  // you can update a remote database when these fire:
  eventAdd: () => console.log('created!'),
  eventChange: handleChange,
  eventRemove: () => console.log('deleted!'),
})

const handleWeekendsToggle = () => {
  calendarOptions.weekends = !calendarOptions.weekends // update a property
}

onBeforeMount(() => {
  fetchScheduleList(month.value)
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
                  ref="cal"
                  class="demo-app-calendar"
                  :options="calendarOptions"
                >
                  <template #eventContent="arg">
                    <b>{{ arg.timeText }} </b>
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

  <FormModal ref="formModal">
    <template #header>
      <v-icon icon="mdi-calendar-clock-outline" size="small" />
      진행 일정 - 이벤트 {{ mode === 'create' ? '등록' : '편집' }}
    </template>
    <template #default>
      <CModalBody>
        <CRow>
          <CCol>
            <CFormInput
              id="event-title"
              v-model="eventTitle"
              type="text"
              placeholder="진행 일정"
              @keydown.enter="eventManagement"
            />
          </CCol>
        </CRow>
      </CModalBody>
      <CModalFooter>
        <CButton color="light" @click="formModal.close()"> 닫기</CButton>
        <CButton
          v-if="mode === 'create'"
          color="primary"
          @click="eventManagement"
        >
          등록
        </CButton>
        <CButton
          v-if="mode === 'update'"
          color="success"
          @click="eventManagement"
        >
          수정
        </CButton>
        <CButton v-if="mode === 'update'" color="danger" @click="removeConfirm">
          삭제
        </CButton>
      </CModalFooter>
    </template>
  </FormModal>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <v-icon icon="mdi-trash-can-outline" size="small" />
      진행 일정 - 이벤트 삭제
    </template>
    [{{ eventTitle }}] - 삭제 후 복구할 수 없습니다. 해당 일정을 삭제
    하시겠습니까?
    <template #footer>
      <CButton color="danger" @click="eventRemove">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
