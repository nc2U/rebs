import dayjs from 'dayjs'

export default {
  methods: {
    numFormat(val: number | null, n?: number) {
      const value = val === null ? 0 : val
      const parts = n
        ? Number(value).toFixed(n).split('.')
        : value.toString().split('.')
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',')
      return !value || value === 0 ? '-' : parts.join('.')
    },

    cutString(str: string, len: number) {
      const content = str ? str : ''
      return content.length > len ? `${content.substr(0, len)}..` : content
    },

    diffDate(date: string) {
      const now = new Date()
      const start = new Date(date)
      const btween = now.getTime() - start.getTime()
      return btween / 1000 / 60 / 60 / 24
    },

    dateFormat(date: Date) {
      return dayjs(date).format('YYYY-MM-DD')
    },
  },
}
