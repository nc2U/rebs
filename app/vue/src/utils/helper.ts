import { createToast, ToastType } from 'mosha-vue-toastify'

export const message = (
  type = 'success' as ToastType,
  title = '알림!',
  description = '해당 내용이 저장되었습니다!',
  duration = 2500,
) => {
  createToast(
    { title, description },
    {
      type,
      hideProgressBar: true,
      showIcon: true,
      timeout: duration,
      transition: 'slide',
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
