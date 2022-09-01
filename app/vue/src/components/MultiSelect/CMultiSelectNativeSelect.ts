import { defineComponent, h, inject, PropType, VNode } from 'vue'
import { Option } from './CMultiSelect'

const CMultiSelectNativeSelect = defineComponent({
  name: 'CMultiSelectGroupOption',
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
     * List of option elements.
     */
    options: {
      type: Array as PropType<Option[]>,
      default: () => [],
      required: false,
    },
    value: {
      type: [Number, String, Array],
      default: undefined,
      require: false,
    },
  },
  emits: ['change'],
  setup(props, { emit }) {
    const nativeSelectRef = inject('nativeSelectRef') as any
    const createNativeOptions = (options: Option[]): VNode | VNode[] => {
      return options.map((option: Option) => {
        return option.options
          ? h('optgroup', { label: option.label }, createNativeOptions(option.options))
          : h('option', { disabled: option.disabled, value: option.value })
      })
    }
    const handleChange = (event: Event) => {
      const target = event.target as HTMLSelectElement
      emit('change', Number(target.value))
    }

    return () =>
      h(
        'select',
        {
          multiple: props.multiple,
          tabIndex: '-1',
          style: { display: 'none' },
          value: props.value,
          ref: nativeSelectRef,
          onChange: handleChange,
        },
        props.options && createNativeOptions(props.options),
      )
  },
})

export { CMultiSelectNativeSelect }
