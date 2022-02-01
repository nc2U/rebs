import { createToast } from 'mosha-vue-toastify'

export function message(
  type: any = 'success',
  title: any = '알림!',
  description: any = '해당 내용이 저장되었습니다!',
) {
  createToast(
    {
      title,
      description,
    },
    {
      type,
      hideProgressBar: true,
      showIcon: true,
      transition: 'slide',
      // toastBackgroundColor: '#4DC374',
    },
  )
}
