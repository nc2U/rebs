import { defineComponent } from 'vue'

export default defineComponent({
  methods: {
    numFormat(value: number, n?: number) {
      const parts = n
        ? Number(value).toFixed(n).split('.')
        : value.toString().split('.')
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',')
      return !value || value === 0 ? '-' : parts.join('.')
    },
    areaM2Format(value: number, n = 2) {
      return !value || value === 0 ? '-' : `${this.numFormat(value, n)} ㎡`
    },
    areaPyFormat(value: number, n = 2) {
      return !value || value === 0
        ? '-'
        : `${this.numFormat(value * 0.3025, n)} 평`
    },
    areaM2PyFormat(value: number, n = 2) {
      return !value || value === 0
        ? '-'
        : `${this.numFormat(value, n)} ㎡ (${this.numFormat(
            value * 0.3025,
            n,
          )} 평)`
    },
    ratioFormat(value: number, n = 2) {
      return !value || value === 0 ? '-' : `${this.numFormat(value, n)} %`
    },
  },
})
