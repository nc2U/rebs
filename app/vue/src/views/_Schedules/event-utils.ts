import { EventInput } from '@fullcalendar/vue3'

let eventGuid = 0
const todayStr: string = new Date().toISOString().replace(/T.*$/, '') // YYYY-MM-DD of today

export const INITIAL_EVENTS: EventInput[] = [
  {
    id: '1',
    title: 'All-day event',
    start: todayStr,
  },
  {
    id: '2',
    title: 'Timed event',
    start: todayStr + 'T12:00:00',
  },
  {
    id: '3',
    title: 'Tomorrow eventaasdfasdf',
    start: '2022-08-08',
  },
]

export function createEventId() {
  return String(eventGuid++)
}
