export const numFormat = (val: number | string, n?: number, zero: string | 0 = '-') => {
  const value = typeof val === 'number' ? val : parseInt(val) || 0
  const parts = n ? value.toFixed(n).split('.') : value.toString().split('.')
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  return !value || value === 0 ? zero : parts.join('.')
}

export const cutString = (str = '', len = 0) =>
  str.length > len ? `${str.substring(0, len)}..` : str

export const diffDate = (date1: Date | string, date2?: Date) => {
  const start = typeof date1 === 'string' ? new Date(date1) : date1
  const now = !date2 ? new Date() : date2
  const between = now.getTime() - start.getTime()
  return between / 1000 / 60 / 60 / 24
}

export const addDays = (date: Date, days: number) => date.setDate(date.getDate() + days)

export const dateFormat = (date: Date | string) =>
  typeof date === 'string' ? date : date.toISOString().replace(/T.*$/, '')

export const getToday = () =>
  new Date(new Date().getTime() + 32400000).toISOString().replace(/T.*$/, '')

export const timeFormat = (date: Date | number | string) =>
  new Date(+new Date(date) + 32400000).toISOString().replace('T', ' ').replace(/\..*/, '')

export const elapsedTime = (date: number | string): string => {
  const start = new Date(date)
  const end = new Date()

  const seconds = Math.floor((end.getTime() - start.getTime()) / 1000)
  if (seconds < 60) return '방금 전'

  const minutes = seconds / 60
  if (minutes < 60) return `${Math.floor(minutes)}분 전`

  const hours = minutes / 60
  if (hours < 24) return `${Math.floor(hours)}시간 전`

  const days = hours / 24
  if (days < 7) return `${Math.floor(days)}일 전`

  return timeFormat(date)
}
