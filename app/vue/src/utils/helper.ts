import { createToast } from 'mosha-vue-toastify'

export const message = (
  type: any = 'success',
  title: any = '알림!',
  description: any = '해당 내용이 저장되었습니다!',
  duration = 2500,
) => {
  createToast(
    {
      title,
      description,
    },
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

export const errorHandle = (error: any) => {
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

export const isValidate = (event: any) => {
  const el = event.currentTarget
  if (el.checkValidity() === false) {
    event.preventDefault()
    event.stopPropagation()

    return true
  } else return false
}
