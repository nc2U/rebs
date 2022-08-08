export const numFormat = (val = 0, n?: number) => {
  const value = !val ? 0 : val
  const parts = n
    ? Number(value).toFixed(n).split('.')
    : value.toString().split('.')
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  return !value || value === 0 ? '-' : parts.join('.')
}

export const cutString = (str: string, len: number) => {
  const content = str || ''
  return content.length > len ? `${content.substr(0, len)}..` : content
}

export const diffDate = (date1: Date | string, date2?: Date) => {
  const start = typeof date1 === 'string' ? new Date(date1) : date1
  const now = !date2 ? new Date() : date2
  const between = now.getTime() - start.getTime()
  return between / 1000 / 60 / 60 / 24
}

export const addDays = (date: Date, days: number) => {
  return date.setDate(date.getDate() + days)
}

export const dateFormat = (date: Date) => {
  return date.toISOString().replace(/T.*$/, '')
}
