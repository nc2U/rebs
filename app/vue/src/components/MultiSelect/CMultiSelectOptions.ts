import { defineComponent, h, PropType, VNode } from 'vue'
import { Option } from './CMultiSelect'

const CMultiSelectOptions = defineComponent({
  name: 'CMultiSelectOptions',
  props: {
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
     * Sets the label for no results when filtering.
     */
    searchNoResultsLabel: {
      type: String,
      default: 'no items',
      required: false,
    },
  },
  emits: ['optionClick'],
  setup(props, { emit }) {
    const handleOptionClick = (option: Option) => {
      emit('optionClick', option as Option)
    }
    const createOptions = (options: Option[]): VNode | VNode[] => {
      return options.length > 0
        ? options.map((option: Option) => {
            return option.options
              ? h('div', { class: 'form-multi-select-options' }, [
                  h('div', { class: 'form-multi-select-optgroup-label' }, option.label),
                  createOptions(option.options),
                ])
              : h(
                  'div',
                  {
                    class: [
                      'form-multi-select-option',
                      {
                        'form-multi-select-option-with-checkbox': props.optionsStyle === 'checkbox',
                        'form-multi-selected': option.selected,
                        disabled: option.disabled,
                      },
                    ],
                    onClick: () => handleOptionClick(option),
                  },
                  option.text,
                )
          })
        : h('div', { class: 'form-multi-select-options-empty' }, props.searchNoResultsLabel)
    }
    return () =>
      h(
        'div',
        {
          class: 'form-multi-select-options',
          ...(props.optionsMaxHeight !== 'auto' && {
            style: { maxHeight: props.optionsMaxHeight, overflow: 'scroll' },
          }),
        },
        createOptions(props.options),
      )
  },
})

export { CMultiSelectOptions }
