/**
 * --------------------------------------------------------------------------
 * CoreUI PRO (v4.3.1): picker.js
 * License (https://coreui.io/pro/license-new/)
 * --------------------------------------------------------------------------
 */

import EventHandler from './dom/event-handler'
import Manipulator from './dom/manipulator'
import BaseComponent from './base-component'
import Dropdown from './dropdown'

/**
 * ------------------------------------------------------------------------
 * Constants
 * ------------------------------------------------------------------------
 */

const NAME = 'picker'
const DATA_KEY = 'coreui.picker'
const EVENT_KEY = `.${DATA_KEY}`

const EVENT_CANCEL = `onCancelClick${EVENT_KEY}`

const Default = {
  cancelButton: 'Cancel',
  cancelButtonClasses: ['btn', 'btn-sm', 'btn-ghost-primary'],
  confirmButton: 'OK',
  confirmButtonClasses: ['btn', 'btn-sm', 'btn-primary'],
  container: 'dropdown',
  disabled: false,
  footer: false,
}

const DefaultType = {
  cancelButton: '(boolean|string)',
  cancelButtonClasses: '(array|string)',
  confirmButton: '(boolean|string)',
  confirmButtonClasses: '(array|string)',
  container: 'string',
  disabled: 'boolean',
  footer: 'boolean',
}

/**
 * ------------------------------------------------------------------------
 * Class Definition
 * ------------------------------------------------------------------------
 */

class Picker extends BaseComponent {
  constructor(element, config) {
    super(element)

    this._config = this._getConfig(config)
    this._dropdown = null

    //
    this._dropdownEl = null
    this._dropdownMenuEl = null
    this._dropdownToggleEl = null

    this._createPicker()
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

  _getButtonClasses(classes) {
    if (typeof classes === 'string') {
      return classes.split(' ')
    }

    return classes
  }

  // Private
  _createDropdown() {
    const dropdownEl = document.createElement('div')
    dropdownEl.classList.add('picker')
    this._dropdownEl = dropdownEl

    const dropdownToggleEl = document.createElement('div')
    this._dropdownToggleEl = dropdownToggleEl

    if (!this._config.disabled) {
      Manipulator.setDataAttribute(dropdownToggleEl, 'toggle', 'dropdown')
    }

    const dropdownMenuEl = document.createElement('div')
    dropdownMenuEl.classList.add('dropdown-menu')
    this._dropdownMenuEl = dropdownMenuEl

    dropdownEl.append(dropdownToggleEl, dropdownMenuEl)

    this._element.append(dropdownEl)

    this._dropdown = new Dropdown(dropdownToggleEl, {
      autoClose: 'outside',
    })
  }

  _createFooter() {
    const footerEl = document.createElement('div')
    footerEl.classList.add('picker-footer')

    footerEl.append(this._createFooterContent())

    if (this._config.cancelButton) {
      const cancelButtonEl = document.createElement('button')
      cancelButtonEl.classList.add(
        ...this._getButtonClasses(this._config.cancelButtonClasses),
      )
      cancelButtonEl.type = 'button'
      cancelButtonEl.innerHTML = this._config.cancelButton
      cancelButtonEl.addEventListener('click', () => {
        this._dropdown.hide()
        EventHandler.trigger(this._element, EVENT_CANCEL)
      })

      footerEl.append(cancelButtonEl)
    }

    if (this._config.confirmButton) {
      const confirmButtonEl = document.createElement('button')
      confirmButtonEl.classList.add(
        ...this._getButtonClasses(this._config.confirmButtonClasses),
      )
      confirmButtonEl.type = 'button'
      confirmButtonEl.innerHTML = this._config.confirmButton
      confirmButtonEl.addEventListener('click', () => {
        this._dropdown.hide()
      })

      footerEl.append(confirmButtonEl)
    }

    this._dropdownMenuEl.append(footerEl)
  }

  _createFooterContent() {
    return ''
  }

  _createPicker() {
    if (this._config.container === 'dropdown') {
      this._createDropdown()
    }

    if (this._config.footer || this._config.timepicker) {
      this._createFooter()
    }
  }

  _getConfig(config) {
    config = {
      ...this.constructor.Default,
      ...Manipulator.getDataAttributes(this._element),
      ...(typeof config === 'object' ? config : {}),
    }

    return config
  }
}

export default Picker
