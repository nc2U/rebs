/* eslint-disable indent, multiline-ternary */
/**
 * --------------------------------------------------------------------------
 * CoreUI PRO (v4.3.1): calendar.js
 * License (https://coreui.io/pro/license-new/)
 * --------------------------------------------------------------------------
 */

import { defineJQueryPlugin } from './util/index'
import EventHandler from './dom/event-handler'
import Manipulator from './dom/manipulator'
import {
  createGroupsInArray,
  getMonthDetails,
  getMonthsNames,
  getYears,
  isDateDisabled,
  isDateInRange,
  isDateSelected,
  isLastDayOfMonth,
  isToday,
  isStartDate,
  isEndDate,
} from './util/calendar'
import BaseComponent from './base-component'

/**
 * ------------------------------------------------------------------------
 * Constants
 * ------------------------------------------------------------------------
 */

const NAME = 'calendar'
const DATA_KEY = 'coreui.calendar'
const EVENT_KEY = `.${DATA_KEY}`
const DATA_API_KEY = '.data-apiV1'

const EVENT_CALENDAR_DATE_CHANGE = `calendarDateChange${EVENT_KEY}`
const EVENT_CELL_HOVER = `cellHover${EVENT_KEY}`
const EVENT_END_DATE_CHANGE = `endDateChange${EVENT_KEY}`
const EVENT_LOAD_DATA_API = `load${EVENT_KEY}${DATA_API_KEY}`
const EVENT_MOUSEENTER = `mouseenter${EVENT_KEY}`
const EVENT_MOUSELEAVE = `mouseleave${EVENT_KEY}`
const EVENT_START_DATE_CHANGE = `startDateChange${EVENT_KEY}`

const CLASS_NAME_CALENDAR = 'calendar'

const SELECTOR_CALENDAR = '.calendar'
const SELECTOR_CALENDAR_CELL_INNER = '.calendar-cell-inner'

const Default = {
  calendarDate: new Date(),
  calendars: 1,
  disabledDates: null,
  endDate: null,
  firstDayOfWeek: 1,
  locale: 'default',
  maxDate: null,
  minDate: null,
  range: true,
  startDate: null,
  selectEndDate: false,
  weekdayFormat: 2,
}

const DefaultType = {
  calendarDate: '(date|string|null)',
  calendars: 'number',
  disabledDates: '(array|null)',
  endDate: '(date|string|null)',
  firstDayOfWeek: 'number',
  locale: 'string',
  maxDate: '(date|string|null)',
  minDate: '(date|string|null)',
  range: 'boolean',
  startDate: '(date|string|null)',
  selectEndDate: 'boolean',
  weekdayFormat: '(number|string)',
}

/**
 * ------------------------------------------------------------------------
 * Class Definition
 * ------------------------------------------------------------------------
 */

class Calendar extends BaseComponent {
  constructor(element, config) {
    super(element)

    this._config = this._getConfig(config)
    this._calendarDate = this._config.calendarDate
    this._startDate = this._config.startDate
    this._endDate = this._config.endDate
    this._hoverDate = null
    this._selectEndDate = this._config.selectEndDate
    this._view = 'days'

    this._createCalendar()
    this._addEventListeners()
  }

  // Getters

  static get Default() {
    return Default
  }

  static get DefaultType() {
    return DefaultType
  }

  static get NAME() {
    return NAME
  }

  // Private
  _addEventListeners() {
    EventHandler.on(
      this._element,
      'click',
      SELECTOR_CALENDAR_CELL_INNER,
      event => {
        event.preventDefault()
        if (event.target.classList.contains('day')) {
          this._selectDate(Manipulator.getDataAttribute(event.target, 'date'))
        }

        if (event.target.classList.contains('month')) {
          this._setCalendarDate(
            new Date(
              this._calendarDate.getFullYear(),
              Manipulator.getDataAttribute(event.target, 'month'),
              1,
            ),
          )
          this._view = 'days'
        }

        if (event.target.classList.contains('year')) {
          this._calendarDate = new Date(
            Manipulator.getDataAttribute(event.target, 'year'),
            this._calendarDate.getMonth(),
            1,
          )
          this._view = 'months'
        }

        this._updateCalendar()
      },
    )

    EventHandler.on(
      this._element,
      EVENT_MOUSEENTER,
      SELECTOR_CALENDAR_CELL_INNER,
      event => {
        event.preventDefault()
        if (event.target.parentElement.classList.contains('disabled')) {
          return
        }

        this._hoverDate = new Date(
          Manipulator.getDataAttribute(event.target, 'date'),
        )

        EventHandler.trigger(this._element, EVENT_CELL_HOVER, {
          date: new Date(Manipulator.getDataAttribute(event.target, 'date')),
        })
      },
    )

    EventHandler.on(
      this._element,
      EVENT_MOUSELEAVE,
      SELECTOR_CALENDAR_CELL_INNER,
      event => {
        event.preventDefault()

        this._hoverDate = null

        EventHandler.trigger(this._element, EVENT_CELL_HOVER, {
          date: null,
        })
      },
    )

    // Navigation
    EventHandler.on(this._element, 'click', '.btn-prev', event => {
      event.preventDefault()
      this._modifyCalendarDate(0, -1)
    })

    EventHandler.on(this._element, 'click', '.btn-double-prev', event => {
      event.preventDefault()
      this._modifyCalendarDate(this._view === 'years' ? -10 : -1)
    })

    EventHandler.on(this._element, 'click', '.btn-next', event => {
      event.preventDefault()
      this._modifyCalendarDate(0, 1)
    })

    EventHandler.on(this._element, 'click', '.btn-double-next', event => {
      event.preventDefault()
      this._modifyCalendarDate(this._view === 'years' ? 10 : 1)
    })

    EventHandler.on(this._element, 'click', '.btn-month', event => {
      event.preventDefault()
      this._view = 'months'
      this._element.innerHTML = ''
      this._createCalendarPanel()
    })

    EventHandler.on(this._element, 'click', '.btn-year', event => {
      event.preventDefault()
      this._view = 'years'
      this._element.innerHTML = ''
      this._createCalendarPanel()
    })
  }

  _setCalendarDate(date) {
    this._calendarDate = date

    EventHandler.trigger(this._element, EVENT_CALENDAR_DATE_CHANGE, {
      date,
    })
  }

  _modifyCalendarDate(years, months = 0) {
    const year = this._calendarDate.getFullYear()
    const month = this._calendarDate.getMonth()
    const d = new Date(year, month, 1)

    if (years) {
      d.setFullYear(d.getFullYear() + years)
    }

    if (months) {
      d.setMonth(d.getMonth() + months)
    }

    this._calendarDate = d

    if (this._view === 'days') {
      EventHandler.trigger(this._element, EVENT_CALENDAR_DATE_CHANGE, {
        date: d,
      })
    }

    this._updateCalendar()
  }

  _setEndDate(date, selectEndDate = false) {
    this._endDate = new Date(date)
    EventHandler.trigger(this._element, EVENT_END_DATE_CHANGE, {
      date: this._endDate,
      selectEndDate,
    })
  }

  _setStartDate(date, selectEndDate = true) {
    this._startDate = new Date(date)
    EventHandler.trigger(this._element, EVENT_START_DATE_CHANGE, {
      date: this._startDate,
      selectEndDate,
    })
  }

  _selectDate(date) {
    if (
      isDateDisabled(
        date,
        this._config.minDate,
        this._config.maxDate,
        this._config.disabledDates,
      )
    ) {
      return
    }

    if (this._config.range) {
      if (this._selectEndDate) {
        if (this._startDate && this._startDate > new Date(date)) {
          this._setEndDate(this._startDate)
          this._setStartDate(date)
        } else {
          this._setEndDate(date)
        }
      } else {
        this._setStartDate(date, true)
      }
    } else {
      this._setStartDate(date)
    }
  }

  _createCalendarPanel(addMonths) {
    let date = this._calendarDate

    if (addMonths !== 0) {
      date = new Date(
        this._calendarDate.getFullYear(),
        this._calendarDate.getMonth() + addMonths,
        1,
      )
    }

    const year = date.getFullYear()
    const month = date.getMonth()

    const calendarPanelEl = document.createElement('div')
    calendarPanelEl.classList.add('calendar-panel')

    // Create navigation
    const navigationElement = document.createElement('div')
    navigationElement.classList.add('calendar-nav')
    navigationElement.innerHTML = `
      <div class="calendar-nav-prev">
        <button class="btn btn-transparent btn-sm btn-double-prev">
          <span class="calendar-nav-icon calendar-nav-icon-double-prev"></span>
        </button>
        ${
          this._view === 'days'
            ? `<button class="btn btn-transparent btn-sm btn-prev">
          <span class="calendar-nav-icon calendar-nav-icon-prev"></span>
        </button>`
            : ''
        }
      </div>
      <div class="calendar-nav-date">
        <button class="btn btn-transparent btn-sm btn-month">
          ${date.toLocaleDateString(this._config.locale, { month: 'long' })}
        </button>
        <button class="btn btn-transparent btn-sm btn-year">
          ${date.toLocaleDateString(this._config.locale, { year: 'numeric' })}
        </button>
      </div>
      <div class="calendar-nav-next">
        ${
          this._view === 'days'
            ? `<button class="btn btn-transparent btn-sm btn-next">
          <span class="calendar-nav-icon calendar-nav-icon-next"></span>
        </button>`
            : ''
        }
        <button class="btn btn-transparent btn-sm btn-double-next">
          <span class="calendar-nav-icon calendar-nav-icon-double-next"></span>
        </button>
      </div>
    `

    const monthDetails = getMonthDetails(
      year,
      month,
      this._config.firstDayOfWeek,
    )
    const listOfMonths = createGroupsInArray(
      getMonthsNames(this._config.locale),
      4,
    )
    const listOfYears = createGroupsInArray(getYears(date.getFullYear()), 4)
    const weekDays = monthDetails[0]

    const calendarTable = document.createElement('table')
    calendarTable.innerHTML = `
    ${
      this._view === 'days'
        ? `
      <thead>
        <tr>
          ${weekDays
            .map(
              ({ date }) =>
                `<th class="calendar-cell">
              <div class="calendar-header-cell-inner">
              ${
                typeof this._config.weekdayFormat === 'string'
                  ? date.toLocaleDateString(this._config.locale, {
                      weekday: this._config.weekdayFormat,
                    })
                  : date
                      .toLocaleDateString(this._config.locale, {
                        weekday: 'long',
                      })
                      .slice(0, this._config.weekdayFormat)
              }
              </div>
            </th>`,
            )
            .join('')}
        </tr>
      </thead>`
        : ''
    }
      <tbody>
        ${
          this._view === 'days'
            ? monthDetails
                .map(
                  week =>
                    `<tr>${week
                      .map(
                        ({ date, month }) =>
                          `<td class="calendar-cell ${this._dayClassNames(
                            date,
                            month,
                          )}">
              <div class="calendar-cell-inner day" data-coreui-date="${date}">
                ${date.toLocaleDateString(this._config.locale, {
                  day: 'numeric',
                })}
              </div>
            </td>`,
                      )
                      .join('')}</tr>`,
                )
                .join('')
            : ''
        }
        ${
          this._view === 'months'
            ? listOfMonths
                .map(
                  (row, index) =>
                    `<tr>${row
                      .map(
                        (month, idx) =>
                          `<td class="calendar-cell">
              <div class="calendar-cell-inner month" data-coreui-month="${
                index * 3 + idx - addMonths
              }">
                ${month}
              </div>
            </td>`,
                      )
                      .join('')}</tr>`,
                )
                .join('')
            : ''
        }
        ${
          this._view === 'years'
            ? listOfYears
                .map(
                  row =>
                    `<tr>${row
                      .map(
                        year =>
                          `<td class="calendar-cell">
              <div class="calendar-cell-inner year" data-coreui-year="${year}">
                ${year}
              </div>
            </td>`,
                      )
                      .join('')}</tr>`,
                )
                .join('')
            : ''
        }
      </tbody>
    `
    calendarPanelEl.append(navigationElement, calendarTable)

    return calendarPanelEl
  }

  _createCalendar() {
    const calendarsEl = document.createElement('div')
    calendarsEl.classList.add('calendars')
    // eslint-disable-next-line no-unused-vars
    for (const [index, _] of Array.from({
      length: this._config.calendars,
    }).entries()) {
      calendarsEl.append(this._createCalendarPanel(index))
    }

    this._element.classList.add(CLASS_NAME_CALENDAR)
    this._element.append(calendarsEl)
  }

  _updateCalendar() {
    this._element.innerHTML = ''
    this._createCalendarPanel()
  }

  _dayClassNames(date, month) {
    const classNames = {
      today: isToday(date),
      disabled: isDateDisabled(
        date,
        this._config.minDate,
        this._config.maxDate,
        this._config.disabledDates,
      ),
      [month]: true,
      last: isLastDayOfMonth(date),
      range:
        month === 'current' &&
        isDateInRange(date, this._startDate, this._endDate),
      'range-hover':
        month === 'current' &&
        (this._hoverDate && this._selectEndDate
          ? isDateInRange(date, this._startDate, this._hoverDate)
          : isDateInRange(date, this._hoverDate, this._endDate)),
      selected: isDateSelected(date, this._startDate, this._endDate),
      start: isStartDate(date, this._startDate, this._endDate),
      end: isEndDate(date, this._startDate, this._endDate),
    }

    // eslint-disable-next-line unicorn/no-array-reduce
    const result = Object.keys(classNames).reduce((o, key) => {
      // eslint-disable-next-line no-unused-expressions
      classNames[key] === true && (o[key] = classNames[key])
      return o
    }, {})

    return Object.keys(result).join(' ')
  }

  _getConfig(config) {
    config = {
      ...this.constructor.Default,
      ...Manipulator.getDataAttributes(this._element),
      ...config,
    }

    return config
  }

  // Static

  static calendarInterface(element, config) {
    const data = Calendar.getOrCreateInstance(element, config)

    if (typeof config === 'string') {
      if (typeof data[config] === 'undefined') {
        throw new TypeError(`No method named "${config}"`)
      }

      data[config]()
    }
  }

  static jQueryInterface(config) {
    return this.each(function () {
      const data = Calendar.getOrCreateInstance(this)

      if (typeof config !== 'string') {
        return
      }

      if (
        data[config] === undefined ||
        config.startsWith('_') ||
        config === 'constructor'
      ) {
        throw new TypeError(`No method named "${config}"`)
      }

      data[config](this)
    })
  }
}

/**
 * ------------------------------------------------------------------------
 * Data Api implementation
 * ------------------------------------------------------------------------
 */

EventHandler.on(window, EVENT_LOAD_DATA_API, () => {
  for (const element of Array.from(
    document.querySelectorAll(SELECTOR_CALENDAR),
  )) {
    Calendar.calendarInterface(element)
  }
})

/**
 * ------------------------------------------------------------------------
 * jQuery
 * ------------------------------------------------------------------------
 * add .Calendar to jQuery only if jQuery is present
 */

defineJQueryPlugin(Calendar)

export default Calendar
