interface AddressData {
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

const addressMixin = {
  data() {
    return {
      addrForm: null,
      zipcode: '',
      address1: '',
      address3: '',
    }
  },
  methods: {
    addressPut(this: any, data: AddressData) {
      // 각 주소의 노출 규칙에 따라 주소를 조합한다. 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
      let mainAddr = '' // 주소 변수
      let extraAddr = '' // 참고항목 변수

      //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
      if (data.userSelectedType === 'R') {
        mainAddr = data.roadAddress // 사용자가 도로명 주소를 선택했을 경우
      } else {
        mainAddr = data.jibunAddress // 사용자가 지번 주소를 선택했을 경우(J)
      }

      // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
      if (data.userSelectedType === 'R') {
        // 법정동명이 있을 경우 추가한다. (법정리는 제외), 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
        if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
          extraAddr = data.bname
        }
        // 건물명이 있고, 공동주택일 경우 추가한다.
        if (data.buildingName !== '' && data.apartment === 'Y') {
          extraAddr +=
            extraAddr !== '' ? ', ' + data.buildingName : data.buildingName
        }
        // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
        if (extraAddr !== '') {
          extraAddr = ' (' + extraAddr + ')'
        }
      }

      this.addrForm = data.formNum
      this.zipcode = data.zonecode // 우편번호와 주소 정보를 해당 필드에 넣는다.
      this.address1 = mainAddr
      this.address3 = extraAddr // 조합된 참고항목을 해당 필드에 넣는다.
    },
  },
  watch: {
    addrForm(this: any, newVal: number) {
      if (newVal === 1) {
        this.form.zipcode = this.zipcode // 우편번호와 주소 정보를 해당 필드에 넣는다.
        this.form.address1 = this.address1
        this.form.address2 = ''
        this.form.address3 = this.address3 // 조합된 참고항목을 해당 필드에 넣는다.
        this.$refs.address2.$el.nextElementSibling.focus() // 커서를 상세주소 필드로 이동한다.
      }
    },
  },
}

export default addressMixin
