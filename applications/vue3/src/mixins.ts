export default {
  methods: {
    numFormat(value: number) {
      return !value || value === 0
        ? '-'
        : value.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ',')
    },
    twoDecimal(value: number) {
      return !value || value === 0
        ? '-'
        : Number(value)
            .toFixed(2)
            .replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ',')
    },
    areaM2Format(value: number) {
      return !value || value === 0 ? '-' : `${this.twoDecimal(value)} ㎡`
    },
    areaPyFormat(value: number) {
      const toVal = Number(value.toFixed(2))
      return !value || value === 0 ? '-' : `${this.twoDecimal(toVal)} 평`
    },
    areaM2PyFormat(value: number) {
      return !value || value === 0
        ? '-'
        : `${this.twoDecimal(value)} ㎡ (${this.twoDecimal(value)} 평)`
    },
    ratioFormat(value: number) {
      return !value || value === 0 ? '-' : `${this.twoDecimal(value)} %`
    },
  },
}
