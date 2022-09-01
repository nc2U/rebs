import { defineComponent, h, onMounted, onUnmounted, PropType, provide, ref, watch } from 'vue'
import { CMultiSelectNativeSelect } from './CMultiSelectNativeSelect'
import { CMultiSelectOptions } from './CMultiSelectOptions'
import { CMultiSelectSelection } from './CMultiSelectSelection'
export interface Option {
  disabled?: boolean
  label?: string
  options?: Option[]
  order?: number
  selected?: boolean
  text: string
  value: number | string
}

const CMultiSelect = defineComponent({
  name: 'CMultiSelect',
  props: {
    /**
     * Enables selection cleaner element.
     *
     * @default true
     */
    cleaner: {
      type: Boolean,
      required: false,
      default: true,
    },
    /**
     * It specifies that multiple options can be selected at once.
     *
     * @default true
     */
    multiple: {
      type: Boolean,
      default: true,
      required: false,
    },
    /**
     * List of option elements.
     */
    options: {
      type: Array as PropType<Option[]>,
      default: () => [],
      required: false,
    },
    /**
     * Sets maxHeight of options list.
     *
     * @default 'auto'
     */
    optionsMaxHeight: {
      type: [Number, String],
      default: 'auto',
      required: false,
    },
    /**
     * Sets option style.
     *
     * @values 'checkbox', 'text'
     * @default 'checkbox'
     */
    optionsStyle: {
      type: String,
      default: 'checkbox',
      required: false,
      validator: (value: string) => {
        return ['checkbox', 'text'].includes(value)
      },
    },
    /**
     * Specifies a short hint that is visible in the search input.
     *
     * @default 'Select...''
     */
    placeholder: {
      type: String,
      default: 'Select...',
      required: false,
    },
    /**
     * Enables search input element.
     */
    search: {
      type: Boolean,
      default: true,
      required: false,
    },
    /**
     * Sets the label for no results when filtering.
     */
    searchNoResultsLabel: {
      type: String,
      default: 'no items',
      required: false,
    },
    /**
     * Enables select all button.
     *
     * @default true
     */
    selectAll: {
      type: Boolean,
      required: false,
      default: true,
    },
    /**
     * Sets the select all button label.
     *
     * @default 'Select all options'
     */
    selectAllLabel: {
      type: String,
      required: false,
      default: 'Select all options',
    },
    /**
     * Sets the selection style.
     *
     * @values 'counter', 'tags', 'text'
     * @default 'tags'
     */
    selectionType: {
      type: String,
      default: 'tags',
      required: false,
      validator: (value: string) => {
        return ['counter', 'tags', 'text'].includes(value)
      },
    },
    /**
     * Sets the counter selection label.
     *
     * @default 'item(s) selected'
     */
    selectionTypeCounterText: {
      type: String,
      default: 'item(s) selected',
      required: false,
    },
    /**
     * Toggle the visibility of multi select dropdown.
     *
     * @default false
     */
    visible: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  emits: [
    /**
     * Execute a function when a user changes the selected option. [docs]
     */
    'change',
  ],
  setup(props, { emit }) {
    const flattenArray = (options: Option[]): Option[] => {
      return options.reduce((acc: Option[], val: Option) => {
        return acc.concat(Array.isArray(val.options) ? flattenArray(val.options) : val)
      }, [])
    }

    const getSelectedOptions = (options: Option[]) => {
      return flattenArray(options).filter((option: Option) => {
        if (option.selected) {
          return option
        }
        return
      })
    }

    const updateOptions = (
      value: number | string,
      _options: Option[] = options.value,
    ): Option[] => {
      return props.multiple && _options
        ? _options &&
            _options.map((option: Option) => {
              count.value = count.value++
              return option.options
                ? { ...option, options: updateOptions(value, option.options) }
                : option.value == value // TODO: find solution
                ? { ...option, selected: !option.selected, order: count.value }
                : { ...option }
            })
        : _options &&
            _options.map((option: Option) => {
              return option.options
                ? { ...option, options: updateOptions(value, option.options) }
                : option.value == value // TODO: find solution
                ? { ...option, selected: true }
                : { ...option, selected: false }
            })
    }

    const toggleAllOptions = (
      options: Option[],
      selected: boolean,
      counter: number = count.value,
    ): Option[] => {
      return options.map((option: Option) => {
        !option.selected && counter++
        count.value = counter
        if (option.options) {
          return {
            ...option,
            options: toggleAllOptions(option.options, selected, counter),
          }
        }
        return option.disabled
          ? { ...option }
          : selected && !option.selected
          ? { ...option, selected: selected, order: counter }
          : { ...option, selected: selected }
      })
    }

    const filterOptionsList = (search: string, _options = vOptions.value) => {
      return search.length
        ? _options &&
            _options.reduce((acc: Option[], val: Option) => {
              const options =
                val.options &&
                val.options.filter(
                  (element) =>
                    element.text && element.text.toLowerCase().includes(search.toLowerCase()),
                )

              if (
                (val.text && val.text.toLowerCase().includes(search.toLowerCase())) ||
                (options && options.length)
              ) {
                acc.push(Object.assign({}, val, options && options.length && { options }))
              }

              return acc
            }, [])
        : options.value
    }

    const multiSelectRef = ref<HTMLDivElement>()
    const nativeSelectRef = ref<HTMLSelectElement>()
    provide('nativeSelectRef', nativeSelectRef)
    const searchRef = ref<HTMLInputElement>()

    const options = ref<Option[]>(props.options)
    const vOptions = ref<Option[]>(props.options)
    const search = ref('')
    const visible = ref(props.visible)

    const selected = ref<Option[]>(getSelectedOptions(props.options))
    const count = ref<number>(0)

    watch(
      () => props.options,
      () => {
        options.value = props.options
      },
    )

    watch(options, () => {
      const _selected = options.value && getSelectedOptions(options.value)

      _selected.sort((a: Option, b: Option) => {
        if (typeof a.order === 'undefined') {
          return -1
        }
        if (b.order && a.order > b.order) return 1
        if (b.order && a.order < b.order) return -1
        return 0
      })

      selected.value = _selected
    })

    watch([options, search], () => {
      vOptions.value = filterOptionsList(search.value, options.value)
    })

    watch(selected, () => {
      nativeSelectRef.value &&
        nativeSelectRef.value.dispatchEvent(new Event('change', { bubbles: true }))
    })

    onMounted(() => {
      window.addEventListener('click', handleClickOutside)
      window.addEventListener('keyup', handleKeyup)
    })

    onUnmounted(() => {
      window.removeEventListener('click', handleClickOutside)
      window.removeEventListener('keyup', handleKeyup)
    })

    const handleKeyup = (event: Event) => {
      if (multiSelectRef.value && !multiSelectRef.value.contains(event.target as HTMLElement)) {
        visible.value = false
      }
    }
    const handleClickOutside = (event: Event) => {
      if (multiSelectRef.value && !multiSelectRef.value.contains(event.target as HTMLElement)) {
        visible.value = false
      }
    }

    const handleSearchChange = (event: InputEvent) => {
      const target = event.target as HTMLInputElement
      search.value = target.value.toLowerCase()
    }

    const handleSearchKeyDown = (event: KeyboardEvent) => {
      if (search.value.length) return
      if (event.key === 'Backspace' || event.key === 'Delete') {
        const last = selected.value.filter((option: Option) => !option.disabled).pop()

        if (last) {
          selected.value = selected.value.filter((option: Option) => option.value !== last.value)
          options.value = updateOptions(last.value)
        }
      }
    }

    const handleOptionClick = (option: Option) => {
      options.value = updateOptions(option.value)
    }

    const handleSelectAll = () => {
      options.value = toggleAllOptions(options.value, true)
    }

    const handleDeselectAll = () => {
      options.value = toggleAllOptions(options.value, false)
    }

    return () => [
      h(CMultiSelectNativeSelect, {
        multiple: props.multiple,
        options: options.value,
        value: props.multiple
          ? selected.value.map((option: Option) => option.value.toString())
          : selected.value.map((option: Option) => option.value)[0],
        onChange: () => emit('change', selected.value),
      }),
      h(
        'div',
        {
          class: [
            'form-multi-select',
            {
              show: visible.value,
              'form-multi-select-selection-tags': props.multiple && props.selectionType === 'tags',
            },
          ],
          onClick: () => {
            visible.value = true
            props.search && searchRef.value && searchRef.value.focus()
          },
          ref: multiSelectRef,
        },
        [
          h(CMultiSelectSelection, {
            multiple: props.multiple,
            onRemove: (option: Option) => handleOptionClick(option),
            search: props.search,
            selected: selected.value,
            selectionType: props.selectionType,
            selectionTypeCounterText: props.selectionTypeCounterText,
          }),
          props.multiple &&
            props.cleaner &&
            selected.value.length > 0 &&
            h('button', {
              type: 'button',
              class: 'form-multi-select-selection-cleaner',
              onClick: () => handleDeselectAll(),
            }),
          props.search &&
            h('input', {
              type: 'text',
              class: 'form-multi-select-search',
              autocomplete: 'off',
              ...(selected.value.length === 0 && { placeholder: props.placeholder }),
              ...(selected.value.length &&
                props.selectionType === 'counter' && {
                  placeholder: `${selected.value.length} ${props.selectionTypeCounterText}`,
                }),
              ...(selected.value.length &&
                !props.multiple && { placeholder: selected.value.map((option) => option.text)[0] }),
              onInput: (event: InputEvent) => handleSearchChange(event),
              onKeydown: (event: KeyboardEvent) => handleSearchKeyDown(event),
              ...(props.multiple &&
                selected.value.length &&
                props.selectionType !== 'counter' && { size: search.value.length + 2 }),
              ref: searchRef,
            }),
          h('div', { class: 'form-multi-select-dropdown' }, [
            props.multiple &&
              props.selectAll &&
              h(
                'button',
                { class: 'form-multi-select-all', onClick: () => handleSelectAll() },
                props.selectAllLabel,
              ),
            h(CMultiSelectOptions, {
              onOptionClick: (option: Option) => handleOptionClick(option),
              options: vOptions.value,
              optionsMaxHeight: props.optionsMaxHeight,
              optionsStyle: props.optionsStyle,
              searchNoResultsLabel: props.searchNoResultsLabel,
            }),
          ]),
        ],
      ),
    ]
  },
})

export { CMultiSelect }
