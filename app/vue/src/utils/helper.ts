import { createToast, ToastType } from 'mosha-vue-toastify'
import { Position, TransitionType } from 'mosha-vue-toastify/dist/types'

export const message = (
  type: ToastType = 'success',
  title = '알림!',
  description = '해당 내용이 저장되었습니다!',
  duration = 2500,
  position: Position = 'top-right',
  transition: TransitionType = 'slide',
) => {
  createToast(
    { title, description },
    {
      type,
      position,
      transition,
      hideProgressBar: true,
      showIcon: true,
      timeout: duration,
      // toastBackgroundColor: '#4DC374',
    },
  )
}

type Error = {
  [key: string]: string | undefined
  name: string
  message: string
  stack?: string
}

export const errorHandle = (error: Error) => {
  console.log(error)
  for (const key in error) {
    message('danger', `${key} - 에러`, `${error[key]}`, 20000)
  }
}

export const hashCode = (s: string) =>
  s.split('').reduce((a, b) => {
    a = (a << 5) - a + b.charCodeAt(0)
    return a & a
  }, 0)

export const isValidate = (event: Event) => {
  const el = event.currentTarget as
    | HTMLInputElement
    | HTMLSelectElement
    | HTMLFormElement
  if (!el.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()

    return true
  } else return false
}

export const formUtility = {
  getFormData(val: any, formData = new FormData(), namespace = '') {
    if (typeof val !== 'undefined' && val !== null) {
      if (val instanceof Date) {
        formData.append(namespace, val.toISOString())
      } else if (val instanceof Array) {
        for (let i = 0; i < val.length; i++) {
          this.getFormData(val[i], formData, namespace + '[' + i + ']')
        }
      } else if (typeof val === 'object' && !(val instanceof File)) {
        for (const propertyName in val) {
          if (val.hasOwnProperty(propertyName)) {
            this.getFormData(
              val[propertyName],
              formData,
              namespace ? `${namespace}[${propertyName}]` : propertyName,
            )
          }
        }
      } else if (val instanceof File) {
        formData.append(namespace, val)
      } else {
        formData.append(namespace, val.toString())
      }
    }
    return formData
  },
}
