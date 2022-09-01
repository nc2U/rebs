import { defineComponent, h, PropType } from 'vue'
import { Option } from './CMultiSelect'

const CMultiSelectSelection = defineComponent({
  name: 'CMultiSelectSelection',
  props: {
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
     * Enables search input element.
     */
    search: {
      type: Boolean,
      required: false,
      default: false,
    },
    selected: {
      type: Array as PropType<Option[]>,
      default: () => [],
      required: false,
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
  },
  emits: ['remove'],
  setup(props, { emit }) {
    const handleRemove = (option: Option) => {
      emit('remove', option as Option)
    }
    return () =>
      h(
        'div',
        {
          class: 'form-multi-select-selection',
        },
        [
          props.multiple &&
            props.selectionType === 'counter' &&
            !props.search &&
            `${props.selected.length} ${props.selectionTypeCounterText}`,
          props.multiple &&
            props.selectionType === 'tags' &&
            props.selected.map((option: Option) => {
              if (props.selectionType === 'tags') {
                return h('span', { class: 'form-multi-select-tag' }, [
                  option.text,
                  !option.disabled &&
                    h(
                      'button',
                      {
                        class: 'form-multi-select-tag-delete close',
                        ariaLabel: 'Close',
                        onClick: () => handleRemove(option),
                      },
                      h('span', { ariaHidden: 'true' }, 'x'),
                    ),
                ])
              }
              return
            }),
          props.multiple &&
            props.selectionType === 'text' &&
            props.selected.map((option) => option.text).join(', '),
          !props.multiple && !props.search && props.selected.map((option) => option.text)[0],
        ],
      )
  },
})

export { CMultiSelectSelection }
