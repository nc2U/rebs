
/* eslint-disable indent */
/**
 * --------------------------------------------------------------------------
 * CoreUI PRO (v4.3.1): time-picker.js
 * License (https://coreui.io/pro/license-new/)
 * --------------------------------------------------------------------------
 */

import { defineJQueryPlugin } from './util/index'
import EventHandler from './dom/event-handler'
import Manipulator from './dom/manipulator'
import SelectorEngine from './dom/selector-engine'
import {
  convert12hTo24h,
  convert24hTo12h,
  getAmPm,
  getListOfHours,
  getListOfMinutes,
  getListOfSeconds,
  isAmPm,
  isValidTime
} from './util/time'
import Picker from './picker'

/**
* ------------------------------------------------------------------------
* Constants
* ------------------------------------------------------------------------
*/

const NAME = 'time-picker'
const DATA_KEY = 'coreui.time-picker'
const EVENT_KEY = `.${DATA_KEY}`
const DATA_API_KEY = '.data-api'

const EVENT_TIME_CHANGE = `timeChange${EVENT_KEY}`
const EVENT_LOAD_DATA_API = `load${EVENT_KEY}${DATA_API_KEY}`

const SELECTOR_DATA_TOGGLE = '[data-coreui-toggle="time-picker"]'

const Default = {
  ...Picker.Default,
  cleaner: true,
  container: 'dropdown',
  disabled: false,
  footer: true,
  indicator: true,
  inputReadOnly: false,
  locale: 'default',
  placeholder: 'Select time',
  size: null,
  time: null,
  variant: 'roll'
}

const DefaultType = {
  ...Picker.DefaultType,
  cleaner: 'boolean',
  indicator: 'boolean',
  inputReadOnly: 'boolean',
  locale: 'string',
  placeholder: 'string',
  size: '(string|null)',
  time: '(date|string|null)',
  variant: 'string'
}

/**
* ------------------------------------------------------------------------
* Class Definition
* ------------------------------------------------------------------------
*/

class TimePicker extends Picker {
  constructor(element, config) {
    super(element)

    this._config = this._getConfig(config)
    this._date = this._convertStringToDate(this._config.time)
    this._initialDate = null
    this._ampm = this._date ? getAmPm(new Date(this._date), this._config.locale) : 'am'

    // subcomponents
    this._input = null
    this._timePickerBody = null

    this._createTimePicker()
    this._createTimePickerSelection()
    this._addEventListeners()

    this._setUpSelects()
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

  // Public

  cancel() {
    this._date = this._initialDate
    this._input.value = this._initialDate ? this._convertStringToDate(this._initialDate).toLocaleTimeString(this._config.locale) : ''
    this._timePickerBody.innerHTML = ''
    this._createTimePickerSelection()
  }

  clear() {
    this._date = null
    this._input.value = ''
    this._timePickerBody.innerHTML = ''
    this._createTimePickerSelection()
  }

  reset() {
    this._date = this._convertStringToDate(this._config.time)
    this._input.value = this._convertStringToDate(this._config.time).toLocaleTimeString(this._config.locale)
    this._timePickerBody.innerHTML = ''
    this._createTimePickerSelection()
  }

  update(config) {
    this._config = this._getConfig(config)
    this._element.innerHTML = ''
    this._createTimePicker()
    this._createTimePickerSelection()
  }

  _getPartOfTime(part) {
    if (this._date === null) {
      return null
    }

    if (part === 'hours') {
      return isAmPm(this._config.locale) ? convert24hTo12h(this._date.getHours()) : this._date.getHours()
    }

    if (part === 'minutes') {
      return this._date.getMinutes()
    }

    if (part === 'seconds') {
      return this._date.getSeconds()
    }

    if (part === 'toggle') {
      return getAmPm(new Date(this._date), this._config.locale)
    }
  }

  _setUpRolls(initial = false) {
    for (const part of Array.from(['hours', 'minutes', 'seconds', 'toggle'])) {
      for (const element of SelectorEngine.find(`[data-coreui-${part}]`, this._element)) {
        if (this._getPartOfTime(part) === Manipulator.getDataAttribute(element, part)) {
          element.classList.add('selected')
          this._scrollTo(element.parentElement, element, initial)

          for (const sibling of element.parentElement.children) {
            // eslint-disable-next-line max-depth
            if (sibling !== element) {
              sibling.classList.remove('selected')
            }
          }
        }
      }
    }
  }

  _setUpSelects() {
    for (const part of Array.from(['hours', 'minutes', 'seconds', 'toggle'])) {
      for (const element of SelectorEngine.find(`select.${part}`, this._element)) {
        if (this._getPartOfTime(part)) {
          element.value = this._getPartOfTime(part)
        }
      }
    }
  }

  // Private
  _addEventListeners() {
    EventHandler.on(this._element, 'shown.coreui.dropdown', () => {
      this._initialDate = new Date(this._date)

      if (this._config.variant === 'roll') {
        this._setUpRolls(true)
      }

      if (this._config.variant === 'select') {
        this._setUpSelects()
      }
    })

    EventHandler.on(this._element, 'timeChange.coreui.time-picker', () => {
      if (this._config.variant === 'roll') {
        this._setUpRolls()
      }

      if (this._config.variant === 'select') {
        this._setUpSelects()
      }
    })

    EventHandler.on(this._element, 'click', '.picker-input-group-cleaner', event => {
      event.stopPropagation()
      this.clear()
    })

    EventHandler.on(this._element, 'onCancelClick.coreui.picker', () => {
      this.cancel()
    })

    EventHandler.on(this._input, 'input', event => {
      if (isValidTime(event.target.value)) {
        this._date = this._convertStringToDate(event.target.value)

        EventHandler.trigger(this._element, EVENT_TIME_CHANGE, {
          timeString: this._date.toTimeString(),
          localeTimeString: this._date.toLocaleTimeString(),
          date: this._date
        })
      }
    })
  }

  _convertStringToDate(date) {
    return date ? (date instanceof Date ? date : new Date(`1970-01-01 ${date}`)) : null
  }

  _createInputGroup() {
    const inputGroupEl = document.createElement('div')
    inputGroupEl.classList.add('input-group', 'picker-input-group')

    if (this._config.size) {
      inputGroupEl.classList.add(`input-group-${this._config.size}`)
    }

    const inputEl = document.createElement('input')
    inputEl.classList.add('form-control')
    inputEl.disabled = this._config.disabled
    inputEl.placeholder = this._config.placeholder
    inputEl.readOnly = this._config.inputReadOnly
    inputEl.type = 'text'
    inputEl.value = this._date ? this._date.toLocaleTimeString(this._config.locale) : ''

    inputGroupEl.append(inputEl)

    const inputGroupTextEl = document.createElement('span')
    inputGroupTextEl.classList.add('input-group-text')
    if (this._config.indicator) {
      inputGroupTextEl.innerHTML = `
        <span class="picker-input-group-indicator">
          <span class="picker-input-group-icon time-picker-input-icon"></span>
        </span>`
    }

    if (this._config.cleaner) {
      inputGroupTextEl.innerHTML += `
        <span class="picker-input-group-cleaner" role="button">
          <span class="picker-input-group-icon time-picker-cleaner-icon"></span>
        </span>`
    }

    if (this._config.indicator || this._config.cleaner) {
      inputGroupEl.append(inputGroupTextEl)
    }

    this._input = inputEl

    return inputGroupEl
  }

  _createTimePicker() {
    this._element.classList.add('time-picker')

    if (this._config.container === 'dropdown') {
      this._dropdownToggleEl.append(this._createInputGroup())
      this._dropdownMenuEl.prepend(this._createTimePickerBody())
    }

    if (this._config.container === 'inline') {
      this._element.append(this._createTimePickerBody())
    }
  }

  _createTimePickerBody() {
    const timePickerBodyEl = document.createElement('div')
    timePickerBodyEl.classList.add('time-picker-body')

    if (this._config.variant === 'roll') {
      timePickerBodyEl.classList.add('time-picker-roll')
    }

    this._timePickerBody = timePickerBodyEl

    return timePickerBodyEl
  }

  _createTimePickerSelection() {
    const selectedHour = this._date ?
    (isAmPm(this._config.locale) ?
      convert24hTo12h(this._date.getHours()) :
      this._date.getHours()) :
    null
    const selectedMinute = this._date ? this._date.getMinutes() : null
    const selectedSecond = this._date ? this._date.getSeconds() : null

    if (this._config.variant === 'roll') {
      this._createTimePickerRoll(selectedHour, selectedMinute, selectedSecond)
    }

    if (this._config.variant === 'select') {
      this._createTimePickerSelect(selectedHour, selectedMinute, selectedSecond)
    }
  }

  _createSelect(className, options) {
    const selectEl = document.createElement('select')
    selectEl.classList.add('form-select', 'form-select-sm', className)
    selectEl.disabled = this._config.disabled
    selectEl.addEventListener('change', event => this._handleTimeChange(className, event.target.value))

    for (const option of options) {
      const optionEl = document.createElement('option')
      optionEl.value = option.value
      optionEl.innerHTML = option.label

      selectEl.append(optionEl)
    }

    return selectEl
  }

  _createTimePickerSelect() {
    const timeSeparatorEl = document.createElement('div')
    timeSeparatorEl.classList.add('time-separator')
    timeSeparatorEl.innerHTML = ':'

    this._timePickerBody.innerHTML = '<span class="time-picker-inline-icon"></span>'
    this._timePickerBody.append(
      this._createSelect('hours', getListOfHours(this._config.locale)),
      timeSeparatorEl.cloneNode(true),
      this._createSelect('minutes', getListOfMinutes(this._config.locale, true)),
      timeSeparatorEl,
      this._createSelect('seconds', getListOfSeconds(this._config.locale, true))
    )

    if (isAmPm(this._config.locale)) {
      this._timePickerBody.append(
        this._createSelect('toggle', [{ value: 'am', label: 'AM' }, { value: 'pm', label: 'PM' }], '_selectAmPm', this._ampm)
      )
    }
  }

  _createTimePickerRoll() {
    this._timePickerBody.append(
      this._createTimePickerRollCol(getListOfHours(this._config.locale), 'hours'),
      this._createTimePickerRollCol(getListOfMinutes(this._config.locale), 'minutes'),
      this._createTimePickerRollCol(getListOfSeconds(this._config.locale), 'seconds')
    )

    if (isAmPm(this._config.locale)) {
      this._timePickerBody.append(
        this._createTimePickerRollCol([{ value: 'am', label: 'AM' }, { value: 'pm', label: 'PM' }], 'toggle', this._ampm)
      )
    }
  }

  _createTimePickerRollCol(options, part) {
    const timePickerRollColEl = document.createElement('div')
    timePickerRollColEl.classList.add('time-picker-roll-col')

    for (const option of options) {
      const timePickerRollCellEl = document.createElement('div')
      timePickerRollCellEl.classList.add('time-picker-roll-cell')
      timePickerRollCellEl.setAttribute('role', 'button')
      timePickerRollCellEl.innerHTML = option.label
      timePickerRollCellEl.addEventListener('click', () => {
        this._handleTimeChange(part, option.value)
      })

      Manipulator.setDataAttribute(timePickerRollCellEl, part, option.value)

      timePickerRollColEl.append(timePickerRollCellEl)
    }

    return timePickerRollColEl
  }

  _getConfig(config) {
    config = {
      ...this.constructor.Default,
      ...Manipulator.getDataAttributes(this._element),
      ...(typeof config === 'object' ? config : {})
    }

    return config
  }

  _handleTimeChange = (set, value) => {
    const _date = this._date || new Date('1970-01-01')

    if (set === 'toggle') {
      if (value === 'am') {
        this._ampm = 'am'
        _date.setHours(_date.getHours() - 12)
      }

      if (value === 'pm') {
        this._ampm = 'pm'
        _date.setHours(_date.getHours() + 12)
      }
    }

    if (set === 'hours') {
      if (isAmPm(this._config.locale)) {
        _date.setHours(convert12hTo24h(this._ampm, Number.parseInt(value, 10)))
      } else {
        _date.setHours(Number.parseInt(value, 10))
      }
    }

    if (set === 'minutes') {
      _date.setMinutes(Number.parseInt(value, 10))
    }

    if (set === 'seconds') {
      _date.setSeconds(Number.parseInt(value, 10))
    }

    if (this._input) {
      this._input.value = _date.toLocaleTimeString(this._config.locale)
    }

    this._date = new Date(_date)

    EventHandler.trigger(this._element, EVENT_TIME_CHANGE, {
      timeString: _date.toTimeString(),
      localeTimeString: _date.toLocaleTimeString(),
      date: _date
    })
  }

  _scrollTo(parent, children, initial = false) {
    parent.scrollTo({ top: children.offsetTop, behavior: initial ? 'instant' : 'smooth' })
  }

  _updateTimePicker() {
    this._element.innerHTML = ''
    this._createTimePicker()
  }

  // Static

  static timePickerInterface(element, config) {
    const data = TimePicker.getOrCreateInstance(element, config)

    if (typeof config === 'string') {
      if (typeof data[config] === 'undefined') {
        throw new TypeError(`No method named "${config}"`)
      }

      data[config]()
    }
  }

  static jQueryInterface(config) {
    return this.each(function () {
      const data = TimePicker.getOrCreateInstance(this)

      if (typeof config !== 'string') {
        return
      }

      if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
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
  const timePickers = SelectorEngine.find(SELECTOR_DATA_TOGGLE)
  for (let i = 0, len = timePickers.length; i < len; i++) {
    TimePicker.timePickerInterface(timePickers[i])
  }
})

/**
* ------------------------------------------------------------------------
* jQuery
* ------------------------------------------------------------------------
* add .TimePicker to jQuery only if jQuery is present
*/

defineJQueryPlugin(TimePicker)

export default TimePicker
