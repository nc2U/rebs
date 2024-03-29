import { createToast, type ToastType, type Position, type TransitionType } from 'mosha-vue-toastify'

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

export const errorHandle = (err: Error) => {
  if (err.code === 'token_not_valid') {
    console.log('token_not_valid')
  } else {
    console.log(err)
    for (const key in err) {
      message('danger', `${key} - 에러`, `${err[key]}`, 10000)
    }
  }
}

export const hashCode = (s: string) =>
  s.split('').reduce((a, b) => {
    a = (a << 5) - a + b.charCodeAt(0)
    return a & a
  }, 0)

export const isValidate = (event: Event) => {
  const el = event.currentTarget as HTMLInputElement | HTMLSelectElement | HTMLFormElement
  if (!el.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()

    return true
  } else return false
}
