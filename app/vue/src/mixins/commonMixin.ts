import { defineComponent } from 'vue'

export default defineComponent({
  methods: {
    areaM2Format(this: any, value: number, n = 2) {
      return !value || value === 0 ? '-' : `${this.numFormat(value, n)} ㎡`
    },
    areaPyFormat(this: any, value: number, n = 2) {
      return !value || value === 0
        ? '-'
        : `${this.numFormat(value * 0.3025, n)} 평`
    },
    areaM2PyFormat(this: any, value: number, n = 2) {
      return !value || value === 0
        ? '-'
        : `${this.numFormat(value, n)} ㎡ (${this.numFormat(
            value * 0.3025,
            n,
          )} 평)`
    },
    ratioFormat(this: any, value: number, n = 2) {
      return !value || value === 0 ? '-' : `${this.numFormat(value, n)} %`
    },
  },
})
