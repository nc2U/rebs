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

export const hashCode = (s: string) =>
  s.split('').reduce((a, b) => {
    a = (a << 5) - a + b.charCodeAt(0)
    return a & a
  }, 0)
