import { numFormat } from '@/utils/baseMixins'

export const areaM2Format = (value: number, n = 2) => {
  return !value || value === 0 ? '-' : `${numFormat(value, n)} ㎡`
}

export const areaPyFormat = (value: number, n = 2) => {
  return !value || value === 0 ? '-' : `${numFormat(value * 0.3025, n)} 평`
}

export const areaM2PyFormat = (value: number, n = 2) => {
  return !value || value === 0
    ? '-'
    : `${numFormat(value, n)} ㎡ (${numFormat(value * 0.3025, n)} 평)`
}

export const ratioFormat = (value: number, n = 2) => {
  return !value || value === 0 ? '-' : `${numFormat(value, n)} %`
}
