export const numFormat = (val: number | string, n?: number) => {
  const value = typeof val === 'number' ? val : parseInt(val) || 0
  const parts = n ? value.toFixed(n).split('.') : value.toString().split('.')
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  return !value || value === 0 ? '-' : parts.join('.')
}

export const cutString = (str = '', len: number) =>
  str.length > len ? `${str.substr(0, len)}..` : str

export const diffDate = (date1: Date | string, date2?: Date) => {
  const start = typeof date1 === 'string' ? new Date(date1) : date1
  const now = !date2 ? new Date() : date2
  const between = now.getTime() - start.getTime()
  return between / 1000 / 60 / 60 / 24
}

export const addDays = (date: Date, days: number) =>
  date.setDate(date.getDate() + days)

export const dateFormat = (date: Date | string) => {
  return typeof date === 'string'
    ? date
    : date.toISOString().replace(/T.*$/, '')
}
