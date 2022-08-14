export interface AddressData {
  address: string
  addressEnglish: string
  addressType: string
  apartment: string
  autoJibunAddress: string
  autoJibunAddressEnglish: string
  autoRoadAddress: string
  autoRoadAddressEnglish: string
  bcode: string
  bname: string
  bname1: string
  bname1English: string
  bname2: string
  bname2English: string
  bnameEnglish: string
  buildingCode: string
  buildingName: string
  formNum: number
  hname: string
  jibunAddress: string
  jibunAddressEnglish: string
  noSelected: string
  postcode: string
  postcode1: string
  postcode2: string
  postcodeSeq: string
  query: string
  roadAddress: string
  roadAddressEnglish: string
  roadname: string
  roadnameCode: string
  roadnameEnglish: string
  sido: string
  sidoEnglish: string
  sigungu: string
  sigunguCode: string
  sigunguEnglish: string
  userLanguageType: string
  userSelectedType: string
  zonecode: string
}

export const callAddress = (data: AddressData) => {
  const form = {
    formNum: 1,
    zipcode: '',
    address1: '',
    address3: '',
  }
  form.formNum = data.formNum
  form.zipcode = data.zonecode

  if (data.userSelectedType === 'R') {
    form.address1 = data.roadAddress // 사용자가 도로명 주소를 선택했을 경우
  } else {
    form.address1 = data.jibunAddress // 사용자가 지번 주소를 선택했을 경우(J)
  }

  if (data.userSelectedType === 'R') {
    // 법정동명이 있을 경우 추가한다. (법정리는 제외), 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
    if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
      form.address3 += data.bname
    }
    if (data.buildingName !== '' && data.apartment === 'Y') {
      // 건물명이 있고, 공동주택일 경우 추가한다.
      form.address3 +=
        form.address3 !== '' ? ', ' + data.buildingName : data.buildingName
    }
    // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
    if (form.address3 !== '') {
      form.address3 = ' (' + form.address3 + ')'
    }
  }
  return form
}
