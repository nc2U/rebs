/**
 * --------------------------------------------------------------------------
 * CoreUI PRO (v4.3.1): multi-select.js
 * License (https://coreui.io/pro/license-new/)
 * --------------------------------------------------------------------------
 */

import { defineJQueryPlugin } from './util/index'
import Data from './dom/data'
import EventHandler from './dom/event-handler'
import Manipulator from './dom/manipulator'
import SelectorEngine from './dom/selector-engine'
import BaseComponent from './base-component'

/**
 * ------------------------------------------------------------------------
 * Constants
 * ------------------------------------------------------------------------
 */

const NAME = 'multi-select'
const DATA_KEY = 'coreui.multi-select'
const EVENT_KEY = `.${DATA_KEY}`
const DATA_API_KEY = '.data-api'

const TAB_KEY = 'Tab'
const RIGHT_MOUSE_BUTTON = 2

const SELECTOR_INPUT = '.form-multi-select-search'
const SELECTOR_OPTGROUP = '.form-multi-select-optgroup'
const SELECTOR_OPTION = '.form-multi-select-option'
const SELECTOR_OPTIONS = '.form-multi-select-options'
const SELECTOR_OPTIONS_EMPTY = '.form-multi-select-options-empty'
const SELECTOR_SELECT = '.form-multi-select'
const SELECTOR_SELECTION = '.form-multi-select-selection'
const SELECTOR_SELECTION_CLEANER = '.form-multi-select-selection-cleaner'

const EVENT_CHANGED = `changed${EVENT_KEY}`
const EVENT_CLICK = `click${EVENT_KEY}`
const EVENT_HIDE = `hide${EVENT_KEY}`
const EVENT_HIDDEN = `hidden${EVENT_KEY}`
const EVENT_KEYDOWN = `keydown${EVENT_KEY}`
const EVENT_KEYUP = `keyup${EVENT_KEY}`
const EVENT_SEARCH = `search${EVENT_KEY}`
const EVENT_SHOW = `show${EVENT_KEY}`
const EVENT_SHOWN = `showN${EVENT_KEY}`
const EVENT_CLICK_DATA_API = `click${EVENT_KEY}${DATA_API_KEY}`
const EVENT_KEYUP_DATA_API = `keyup${EVENT_KEY}${DATA_API_KEY}`
const EVENT_LOAD_DATA_API = `load${EVENT_KEY}${DATA_API_KEY}`

const CLASS_NAME_DISABLED = 'disabled'
const CLASS_NAME_SELECT = 'form-multi-select'
const CLASS_NAME_SELECT_DROPDOWN = 'form-multi-select-dropdown'
const CLASS_NAME_SELECT_MULTIPLE = 'form-multi-select-multiple'
const CLASS_NAME_SELECT_WITH_CLEANER = 'form-multi-select-with-cleaner'
const CLASS_NAME_SELECT_ALL = 'form-multi-select-all'
const CLASS_NAME_OPTGROUP = 'form-multi-select-optgroup'
const CLASS_NAME_OPTGROUP_LABEL = 'form-multi-select-optgroup-label'
const CLASS_NAME_OPTION = 'form-multi-select-option'
const CLASS_NAME_OPTION_WITH_CHECKBOX = 'form-multi-select-option-with-checkbox'
const CLASS_NAME_OPTIONS = 'form-multi-select-options'
const CLASS_NAME_OPTIONS_EMPTY = 'form-multi-select-options-empty'
const CLASS_NAME_SEARCH = 'form-multi-select-search'
const CLASS_NAME_SELECTED = 'form-multi-selected'
const CLASS_NAME_SELECTION = 'form-multi-select-selection'
const CLASS_NAME_SELECTION_CLEANER = 'form-multi-select-selection-cleaner'
const CLASS_NAME_SELECTION_TAGS = 'form-multi-select-selection-tags'
const CLASS_NAME_SHOW = 'show'
const CLASS_NAME_TAG = 'form-multi-select-tag'
const CLASS_NAME_TAG_DELETE = 'form-multi-select-tag-delete'

const CLASS_NAME_LABEL = 'label'

const Default = {
  cleaner: true,
  disabled: false,
  multiple: true,
  placeholder: 'Select...',
  options: false,
  optionsMaxHeight: 'auto',
  optionsStyle: 'checkbox',
  search: false,
  searchNoResultsLabel: 'No results found',
  selectAll: true,
  selectAllLabel: 'Select all options',
  selectionType: 'tags',
  selectionTypeCounterText: 'item(s) selected',
}

const DefaultType = {
  cleaner: 'boolean',
  disabled: 'boolean',
  multiple: 'boolean',
  placeholder: 'string',
  options: '(boolean|array)',
  optionsMaxHeight: '(number|string)',
  optionsStyle: 'string',
  search: 'boolean',
  searchNoResultsLabel: 'string',
  selectAll: 'boolean',
  selectAllLabel: 'string',
  selectionType: 'string',
  selectionTypeCounterText: 'string',
}

/**
 * ------------------------------------------------------------------------
 * Class Definition
 * ------------------------------------------------------------------------
 */

class MultiSelect extends BaseComponent {
  constructor(element, config) {
    super(element, config)

    this._selectAllElement = null
    this._selectionElement = null
    this._selectionCleanerElement = null
    this._searchElement = null
    this._optionsElement = null
    this._clone = null
    this._options = this._getOptions()
    this._search = ''
    this._selection = this._getSelectedOptions(this._options)

    if (this._config.options.length > 0) {
      this._createNativeSelect(this._config.options)
    }

    this._createSelect()
    this._addEventListeners()
    Data.set(this._element, DATA_KEY, this)
  }

  // Getters

  static get Default() {
    return Default
  }

  static get DefaultType() {
    return DefaultType
  }

  static get DATA_KEY() {
    return DATA_KEY
  }

  static get NAME() {
    return NAME
  }

  // Public

  show() {
    EventHandler.trigger(this._element, EVENT_SHOW)
    this._clone.classList.add(CLASS_NAME_SHOW)

    if (this._config.search) {
      SelectorEngine.findOne(SELECTOR_INPUT, this._clone).focus()
    }

    EventHandler.trigger(this._element, EVENT_SHOWN)
  }

  hide() {
    EventHandler.trigger(this._element, EVENT_HIDE)
    this._clone.classList.remove(CLASS_NAME_SHOW)
    EventHandler.trigger(this._element, EVENT_HIDDEN)
  }

  search(text) {
    this._search = text.length > 0 ? text.toLowerCase() : text
    this._filterOptionsList()
    EventHandler.trigger(this._element, EVENT_SEARCH)
  }

  update(config) {
    this._config = this._getConfig(config)
    this._options = this._getOptions()
    this._selection = this._getSelectedOptions(this._options)
    this._clone.remove()
    this._element.innerHTML = ''
    this._createNativeOptions(this._element, this._options)
    this._createSelect()
    this._addEventListeners()
  }

  selectAll(options = this._options) {
    for (const option of options) {
      if (option.disabled) {
        continue
      }

      if (option.label) {
        this.selectAll(option.options)
        continue
      }

      this._selectOption(option.value, option.text)
    }
  }

  deselectAll(options = this._options) {
    for (const option of options) {
      if (option.disabled) {
        continue
      }

      if (option.label) {
        this.deselectAll(option.options)
        continue
      }

      this._deselectOption(option.value)
    }
  }

  getValue() {
    return this._selection
  }

  // Private

  _addEventListeners() {
    EventHandler.on(this._clone, EVENT_CLICK, () => {
      if (!this._config.disabled) {
        this.show()
      }
    })

    EventHandler.on(this._searchElement, EVENT_KEYUP, () => {
      this._onSearchChange(this._searchElement)
    })

    EventHandler.on(this._searchElement, EVENT_KEYDOWN, event => {
      const key = event.keyCode || event.charCode

      if ((key === 8 || key === 46) && event.target.value.length === 0) {
        this._deselectLastOption()
      }
    })

    EventHandler.on(this._selectAllElement, EVENT_CLICK, event => {
      event.preventDefault()
      event.stopPropagation()
      this.selectAll()
    })

    EventHandler.on(this._optionsElement, EVENT_CLICK, event => {
      event.preventDefault()
      event.stopPropagation()
      this._onOptionsClick(event.target)
    })

    EventHandler.on(this._selectionCleanerElement, EVENT_CLICK, event => {
      if (!this._config.disabled) {
        event.preventDefault()
        event.stopPropagation()
        this.deselectAll()
      }
    })

    EventHandler.on(this._optionsElement, EVENT_KEYDOWN, event => {
      const key = event.keyCode || event.charCode

      if (key === 13) {
        this._onOptionsClick(event.target)
        SelectorEngine.findOne(SELECTOR_INPUT, this._clone).focus()
      }
    })
  }

  _getConfig(config) {
    config = {
      ...Default,
      ...Manipulator.getDataAttributes(this._element),
      ...(typeof config === 'object' ? config : {}),
    }

    return config
  }

  _getClassNames() {
    return [...this._element.classList.value.split(' ')]
  }

  _getOptions(node = this._element) {
    if (this._config.options) {
      return this._config.options
    }

    const nodes = Array.from(node.childNodes).filter(
      element =>
        element.nodeName === 'OPTION' || element.nodeName === 'OPTGROUP',
    )
    const options = []

    for (const node of nodes) {
      if (node.nodeName === 'OPTION') {
        options.push({
          value: node.value,
          text: node.innerHTML,
          selected: node.selected,
          disabled: node.disabled,
        })
      }

      if (node.nodeName === 'OPTGROUP') {
        options.push({
          label: node.label,
          options: this._getOptions(node),
        })
      }
    }

    return options
  }

  _getSelectedOptions(options) {
    const selected = []

    for (const e of options) {
      if (typeof e.value === 'undefined') {
        this._getSelectedOptions(e.options)
        continue
      }

      if (e.selected) {
        // Add only the last option if single select
        if (!this._config.multiple) {
          selected.length = 0
        }

        selected.push({
          value: String(e.value),
          text: e.text,
        })
      }
    }

    return selected
  }

  _createNativeSelect(data) {
    this._element.classList.add(CLASS_NAME_SELECT)

    if (this._config.multiple) {
      this._element.setAttribute('multiple', true)
    }

    this._createNativeOptions(this._element, data)
  }

  _createNativeOptions(parentElement, options) {
    for (const option of options) {
      if (typeof option.options !== 'undefined') {
        const optgroup = document.createElement('optgroup')
        optgroup.label = option.label
        this._createNativeOptions(optgroup, option.options)
        parentElement.append(optgroup)
      } else {
        const opt = document.createElement('OPTION')
        opt.value = option.value

        if (option.disabled === true) {
          opt.setAttribute('disabled', 'disabled')
        }

        if (option.selected === true) {
          opt.setAttribute('selected', 'selected')
        }

        opt.innerHTML = option.text
        parentElement.append(opt)
      }
    }
  }

  _hideNativeSelect() {
    this._element.tabIndex = '-1'
    this._element.style.display = 'none'
  }

  _createSelect() {
    const div = document.createElement('div')
    div.classList.add(CLASS_NAME_SELECT)

    if (this._config.disabled) {
      this._element.classList.add(CLASS_NAME_DISABLED)
    }

    for (const className of this._getClassNames()) {
      div.classList.add(className)
    }

    if (this._config.multiple) {
      div.classList.add(CLASS_NAME_SELECT_MULTIPLE)
    }

    if (this._config.multiple && this._config.selectionType === 'tags') {
      div.classList.add(CLASS_NAME_SELECTION_TAGS)
    }

    this._clone = div
    this._element.parentNode.insertBefore(div, this._element.nextSibling)
    this._createSelection()
    this._createSelectionCleaner()

    if (this._config.search) {
      this._createSearchInput()
      this._updateSearch()
    }

    this._createOptionsContainer()
    this._hideNativeSelect()
    this._updateOptionsList()
  }

  _createSelection() {
    const span = document.createElement('span')
    span.classList.add(CLASS_NAME_SELECTION)
    this._clone.append(span)

    this._updateSelection()
    this._selectionElement = span
  }

  _createSelectionCleaner() {
    if (this._config.cleaner && this._config.multiple) {
      const cleaner = document.createElement('button')
      cleaner.classList.add(CLASS_NAME_SELECTION_CLEANER)
      cleaner.style.display = 'none'
      this._clone.append(cleaner)
      this._clone.classList.add(CLASS_NAME_SELECT_WITH_CLEANER)

      this._updateSelectionCleaner()
      this._selectionCleanerElement = cleaner
    }
  }

  _createSearchInput() {
    const input = document.createElement('input')
    input.classList.add(CLASS_NAME_SEARCH)

    if (this._config.disabled) {
      input.disabled = true
    }

    this._searchElement = input
    this._updateSearchSize()

    this._clone.append(input)
  }

  _createOptionsContainer() {
    const dropdownDiv = document.createElement('div')
    dropdownDiv.classList.add(CLASS_NAME_SELECT_DROPDOWN)

    if (this._config.selectAll && this._config.multiple) {
      const selectAll = document.createElement('button')
      selectAll.classList.add(CLASS_NAME_SELECT_ALL)
      selectAll.innerHTML = this._config.selectAllLabel

      this._selectAllElement = selectAll

      dropdownDiv.append(selectAll)
    }

    const optionsDiv = document.createElement('div')
    optionsDiv.classList.add(CLASS_NAME_OPTIONS)

    if (this._config.optionsMaxHeight !== 'auto') {
      optionsDiv.style.maxHeight = `${this._config.optionsMaxHeight}px`
      optionsDiv.style.overflow = 'scroll'
    }

    dropdownDiv.append(optionsDiv)

    this._clone.append(dropdownDiv)

    this._createOptions(optionsDiv, this._options)
    this._optionsElement = optionsDiv
  }

  _createOptions(parentElement, options) {
    for (const option of options) {
      if (typeof option.value !== 'undefined') {
        const optionDiv = document.createElement('div')
        optionDiv.classList.add(CLASS_NAME_OPTION)

        if (option.disabled) {
          optionDiv.classList.add(CLASS_NAME_DISABLED)
        }

        if (this._config.optionsStyle === 'checkbox') {
          optionDiv.classList.add(CLASS_NAME_OPTION_WITH_CHECKBOX)
        }

        optionDiv.dataset.value = String(option.value)
        optionDiv.tabIndex = 0
        optionDiv.innerHTML = option.text
        parentElement.append(optionDiv)
      }

      if (typeof option.label !== 'undefined') {
        const optgroup = document.createElement('div')
        optgroup.classList.add(CLASS_NAME_OPTGROUP)

        const optgrouplabel = document.createElement('div')
        optgrouplabel.innerHTML = option.label
        optgrouplabel.classList.add(CLASS_NAME_OPTGROUP_LABEL)
        optgroup.append(optgrouplabel)

        this._createOptions(optgroup, option.options)
        parentElement.append(optgroup)
      }
    }
  }

  _createTag(value, text) {
    const tag = document.createElement('span')
    tag.classList.add(CLASS_NAME_TAG)
    tag.dataset.value = value
    tag.innerHTML = text

    const closeBtn = document.createElement('button')
    closeBtn.classList.add(CLASS_NAME_TAG_DELETE, 'text-medium-emphasis')
    closeBtn.setAttribute('aria-label', 'Close')
    closeBtn.innerHTML = '<span aria-hidden="true">&times;</span>'

    tag.append(closeBtn)

    EventHandler.on(closeBtn, EVENT_CLICK, event => {
      if (!this._config.disabled) {
        event.preventDefault()
        event.stopPropagation()

        tag.remove()
        this._deselectOption(value)
      }
    })

    return tag
  }

  _onOptionsClick(element) {
    if (
      !element.classList.contains(CLASS_NAME_OPTION) ||
      element.classList.contains(CLASS_NAME_LABEL)
    ) {
      return
    }

    const value = String(element.dataset.value)
    const text = element.textContent

    if (
      this._config.multiple &&
      element.classList.contains(CLASS_NAME_SELECTED)
    ) {
      this._deselectOption(value)
    } else if (
      this._config.multiple &&
      !element.classList.contains(CLASS_NAME_SELECTED)
    ) {
      this._selectOption(value, text)
    } else if (!this._config.multiple) {
      this._selectOption(value, text)
    }

    if (!this._config.multiple) {
      this.hide()
      this.search('')
      this._searchElement.value = null
    }
  }

  _selectOption(value, text) {
    if (!this._config.multiple) {
      this.deselectAll()
    }

    if (this._selection.filter(e => e.value === value).length === 0) {
      this._selection.push({
        value,
        text,
      })
    }

    const nativeOption = SelectorEngine.findOne(
      `option[value="${value}"]`,
      this._element,
    )

    if (nativeOption) {
      nativeOption.selected = true
    }

    const option = SelectorEngine.findOne(
      `[data-value="${value}"]`,
      this._optionsElement,
    )
    if (option) {
      option.classList.add(CLASS_NAME_SELECTED)
    }

    EventHandler.trigger(this._element, EVENT_CHANGED, {
      value: this._selection,
    })

    this._updateSelection()
    this._updateSelectionCleaner()
    this._updateSearch()
    this._updateSearchSize()
  }

  _deselectOption(value) {
    const selected = this._selection.filter(e => e.value !== value)
    this._selection = selected

    SelectorEngine.findOne(
      `option[value="${value}"]`,
      this._element,
    ).selected = false

    const option = SelectorEngine.findOne(
      `[data-value="${value}"]`,
      this._optionsElement,
    )
    if (option) {
      option.classList.remove(CLASS_NAME_SELECTED)
    }

    EventHandler.trigger(this._element, EVENT_CHANGED, {
      value: this._selection,
    })

    this._updateSelection()
    this._updateSelectionCleaner()
    this._updateSearch()
    this._updateSearchSize()
  }

  _deselectLastOption() {
    if (this._selection.length > 0) {
      const last = this._selection.pop()
      this._deselectOption(last.value)
    }
  }

  _updateSelection() {
    const selection = SelectorEngine.findOne(SELECTOR_SELECTION, this._clone)

    if (this._config.multiple && this._config.selectionType === 'counter') {
      selection.innerHTML = `${this._selection.length} ${this._config.selectionTypeCounterText}`
      return
    }

    if (this._config.multiple && this._config.selectionType === 'tags') {
      selection.innerHTML = ''
      for (const e of this._selection) {
        selection.append(this._createTag(e.value, e.text))
      }

      return
    }

    if (this._config.multiple && this._config.selectionType === 'text') {
      selection.innerHTML = this._selection.map(e => e.text).join(', ')
      return
    }

    if (this._selection.length > 0) {
      selection.innerHTML = this._selection[0].text
    }
  }

  _updateSelectionCleaner() {
    if (!this._config.cleaner || this._selectionCleanerElement === null) {
      return
    }

    const selectionCleaner = SelectorEngine.findOne(
      SELECTOR_SELECTION_CLEANER,
      this._clone,
    )

    if (this._selection.length > 0) {
      selectionCleaner.style.removeProperty('display')
      return
    }

    selectionCleaner.style.display = 'none'
  }

  _updateSearch() {
    if (!this._config.search) {
      return
    }

    if (this._selection.length > 0 && !this._config.multiple) {
      this._searchElement.placeholder = this._selection[0].text
      this._selectionElement.style.display = 'none'
      return
    }

    if (
      this._selection.length > 0 &&
      this._config.multiple &&
      this._config.selectionType !== 'counter'
    ) {
      this._searchElement.removeAttribute('placeholder')
      this._selectionElement.style.removeProperty('display')
      return
    }

    if (this._selection.length === 0 && this._config.multiple) {
      this._searchElement.placeholder = this._config.placeholder
      this._selectionElement.style.display = 'none'
      return
    }

    if (this._config.multiple && this._config.selectionType === 'counter') {
      this._searchElement.placeholder = `${this._selection.length} item(s) selected`
      this._selectionElement.style.display = 'none'
    }
  }

  _updateSearchSize(size = 2) {
    if (!this._searchElement || !this._config.multiple) {
      return
    }

    if (
      this._selection.length > 0 &&
      (this._config.selectionType === 'tags' ||
        this._config.selectionType === 'text')
    ) {
      this._searchElement.size = size
      return
    }

    if (
      this._selection.length === 0 &&
      (this._config.selectionType === 'tags' ||
        this._config.selectionType === 'text')
    ) {
      this._searchElement.removeAttribute('size')
    }
  }

  _onSearchChange(element) {
    if (element) {
      this.search(element.value)

      this._updateSearchSize(element.value.length + 1)
    }
  }

  _updateOptionsList(options = this._options) {
    for (const option of options) {
      if (option.label) {
        this._updateOptionsList(option.options)
        continue
      }

      if (option.selected) {
        this._selectOption(option.value, option.text)
      }
    }
  }

  _isVisible(element) {
    const style = window.getComputedStyle(element)
    return style.display !== 'none'
  }

  _filterOptionsList() {
    const options = SelectorEngine.find(SELECTOR_OPTION, this._clone)
    let visibleOptions = 0

    for (const option of options) {
      // eslint-disable-next-line unicorn/prefer-includes
      if (option.textContent.toLowerCase().indexOf(this._search) === -1) {
        option.style.display = 'none'
      } else {
        option.style.removeProperty('display')
        visibleOptions++
      }

      const optgroup = option.closest(SELECTOR_OPTGROUP)
      if (optgroup) {
        // eslint-disable-next-line  unicorn/prefer-array-some
        if (
          SelectorEngine.children(optgroup, SELECTOR_OPTION).filter(element =>
            this._isVisible(element),
          ).length > 0
        ) {
          optgroup.style.removeProperty('display')
        } else {
          optgroup.style.display = 'none'
        }
      }
    }

    if (visibleOptions > 0) {
      if (SelectorEngine.findOne(SELECTOR_OPTIONS_EMPTY, this._clone)) {
        SelectorEngine.findOne(SELECTOR_OPTIONS_EMPTY, this._clone).remove()
      }

      return
    }

    if (visibleOptions === 0) {
      const placeholder = document.createElement('div')
      placeholder.classList.add(CLASS_NAME_OPTIONS_EMPTY)
      placeholder.innerHTML = this._config.searchNoResultsLabel

      if (!SelectorEngine.findOne(SELECTOR_OPTIONS_EMPTY, this._clone)) {
        SelectorEngine.findOne(SELECTOR_OPTIONS, this._clone).append(
          placeholder,
        )
      }
    }
  }

  // Static

  static multiSelectInterface(element, config) {
    const data = MultiSelect.getOrCreateInstance(element, config)

    if (typeof config === 'string') {
      if (typeof data[config] === 'undefined') {
        throw new TypeError(`No method named "${config}"`)
      }

      data[config]()
    }
  }

  static jQueryInterface(config) {
    return this.each(function () {
      MultiSelect.multiSelectInterface(this, config)
    })
  }

  static clearMenus(event) {
    if (
      event &&
      (event.button === RIGHT_MOUSE_BUTTON ||
        (event.type === 'keyup' && event.key !== TAB_KEY))
    ) {
      return
    }

    const selects = SelectorEngine.find(SELECTOR_SELECT)

    for (let i = 0, len = selects.length; i < len; i++) {
      const context = Data.get(selects[i], DATA_KEY)
      const relatedTarget = {
        relatedTarget: selects[i],
      }

      if (event && event.type === 'click') {
        relatedTarget.clickEvent = event
      }

      if (!context) {
        continue
      }

      if (!context._clone.classList.contains(CLASS_NAME_SHOW)) {
        continue
      }

      if (context._clone.contains(event.target)) {
        continue
      }

      context._clone.classList.remove(CLASS_NAME_SHOW)

      EventHandler.trigger(context._element, EVENT_HIDDEN)
    }
  }
}

/**
 * ------------------------------------------------------------------------
 * Data Api implementation
 * ------------------------------------------------------------------------
 */
EventHandler.on(window, EVENT_LOAD_DATA_API, () => {
  for (const ms of SelectorEngine.find(SELECTOR_SELECT)) {
    if (ms.tabIndex !== -1) {
      MultiSelect.multiSelectInterface(ms)
    }
  }
})

EventHandler.on(document, EVENT_CLICK_DATA_API, MultiSelect.clearMenus)
EventHandler.on(document, EVENT_KEYUP_DATA_API, MultiSelect.clearMenus)

/**
 * ------------------------------------------------------------------------
 * jQuery
 * ------------------------------------------------------------------------
 * add .MultiSelect to jQuery only if jQuery is present
 */

defineJQueryPlugin(MultiSelect)

export default MultiSelect
