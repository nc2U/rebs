export const addressPut = (data: any) => {
  const form = {
    addrForm: '',
    zipcode: '',
    address1: '',
    address3: '',
  }
  form.addrForm = data.formNum
  form.zipcode = data.zonecode

  if (data.userSelectedType === 'R') {
    form.address1 = data.roadAddress
  } else {
    form.address1 = data.jibunAddress
  }

  if (data.userSelectedType === 'R') {
    if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
      form.address3 += data.bname
    }
    if (data.buildingName !== '' && data.apartment === 'Y') {
      form.address3 +=
        form.address3 !== '' ? ', ' + data.buildingName : data.buildingName
    }
    if (form.address3 !== '') {
      form.address3 = ' (' + form.address3 + ')'
    }
  }

  console.log(form)

  return form
}

// const addressPut = (data: any) => {
//   // form.value.addrForm = data.formNum
//   form.value.zipcode = data.zonecode
//
//   if (data.userSelectedType === 'R') {
//     form.value.address1 = data.roadAddress // 사용자가 도로명 주소를 선택했을 경우
//   } else {
//     form.value.address1 = data.jibunAddress // 사용자가 지번 주소를 선택했을 경우(J)
//   }
//
//   if (data.userSelectedType === 'R') {
//     // 법정동명이 있을 경우 추가한다. (법정리는 제외), 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
//     if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
//       form.value.address3 = data.bname
//     }
//
//     if (data.buildingName !== '' && data.apartment === 'Y') {
//       // 건물명이 있고, 공동주택일 경우 추가한다.
//       form.value.address3 +=
//         form.value.address3 !== ''
//           ? ', ' + data.buildingName
//           : data.buildingName
//     }
//     // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
//     if (form.value.address3 !== '') {
//       form.value.address3 = ' (' + form.value.address3 + ')'
//     }
//   }
//   form.value.address2 = ''
//   address2.value.$el.nextElementSibling.focus()
// }
