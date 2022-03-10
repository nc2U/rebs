<template>
  <CCard>
    <CForm
      class="needs-validation"
      novalidate
      :validated="validated"
      @submit.prevent="onSubmit"
    >
      <CCardBody>
        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            구분
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormSelect
              v-model="contorForm.status"
              @change="unitReset"
              required
            >
              <option value="">---------</option>
              <option value="1">청약</option>
              <option value="2">계약</option>
            </CFormSelect>
            <CFormFeedback invalid>구분 항목을 선택하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            차수
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormSelect
              v-model="contForm.order_group"
              @change="unitReset"
              required
              :disabled="noStatus"
            >
              <option value="">---------</option>
              <option
                v-for="order in orderGroupList"
                :value="order.pk"
                :key="order.pk"
              >
                {{ order.order_group_name }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>차수그룹을 선택하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            타입
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormSelect
              v-model="contForm.unit_type"
              @change="typeSelect"
              required
              :disabled="contForm.order_group === ''"
            >
              <option value="">---------</option>
              <option
                v-for="type in unitTypeList"
                :value="type.pk"
                :key="type.pk"
              >
                {{ type.name }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>유니트 타입을 선택하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            {{ contLabel }}코드
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormSelect
              v-model="contForm.serial_number"
              @change="contForm.houseunit = ''"
              required
              :disabled="contForm.unit_type === ''"
            >
              <option value="">---------</option>
              <option
                v-for="unit in keyUnitList"
                :value="unit.pk"
                :key="unit.pk"
              >
                {{ unit.unit_code }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>
              {{ contLabel }}코드를 선택하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label" v-if="unitSet">
            동호수
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0" v-if="unitSet">
            <CFormSelect
              v-model="contForm.houseunit"
              required
              :disabled="contForm.serial_number === ''"
            >
              <option value="">---------</option>
              <option
                v-for="house in houseUnitList"
                :value="house.pk"
                :key="house.pk"
              >
                {{ house.__str__ }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>동호수를 선택하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <hr />

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            {{ contLabel }}일자
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <DatePicker
              v-show="contorForm.status === '1'"
              v-model="contorForm.reservation_date"
              v-maska="'####-##-##'"
              placeholder="청약일자"
              :required="contorForm.status === '1'"
              :disabled="noStatus"
            />
            <DatePicker
              v-show="contorForm.status !== '1'"
              v-model="contorForm.contract_date"
              v-maska="'####-##-##'"
              placeholder="계약일자"
              :required="isContract"
              :disabled="noStatus"
            />
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            {{ contLabel }}자명
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="contorForm.name"
              type="text"
              maxlength="20"
              :placeholder="`${contLabel}자명을 입력하세요`"
              required
              :disabled="noStatus"
            />
            <CFormFeedback invalid>
              {{ contLabel }}자명을 입력하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            생년월일
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <DatePicker
              v-model="contorForm.birth_date"
              placeholder="생년월일"
              v-maska="'####-##-##'"
              :required="isContract"
              :disabled="noStatus"
            />
            <CFormFeedback invalid>생년월일 입력하세요.</CFormFeedback>
          </CCol>

          <CCol xs="5" lg="1" class="pt-2 p-0 text-center" v-show="isContract">
            <div class="form-check form-check-inline">
              <input
                v-model="contorForm.gender"
                class="form-check-input"
                id="male"
                type="radio"
                value="M"
                name="gender"
                :required="isContract"
                :disabled="!isContract"
              />
              <label class="form-check-label" for="male">남</label>
            </div>
            <div class="form-check form-check-inline">
              <input
                v-model="contorForm.gender"
                class="form-check-input"
                id="female"
                type="radio"
                value="F"
                name="gender"
                :disabled="!isContract"
              />
              <label class="form-check-label" for="female">여</label>
            </div>
            <CFormFeedback invalid>성별을 선택하세요.</CFormFeedback>
          </CCol>

          <CCol xs="6" lg="2" class="pt-2 p-0" v-show="isContract && isUnion">
            <CFormSwitch
              v-model="contorForm.is_registed"
              id="is_registed"
              label="인가등록여부"
              :disabled="!isContract"
            />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            휴대전화
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="contact.cell_phone"
              v-maska="['###-###-####', '###-####-####']"
              type="text"
              maxlength="13"
              placeholder="휴대전화번호를 선택하세요"
              required
              :disabled="noStatus"
            />
            <CFormFeedback invalid>휴대전화번호를 입력하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            집전화
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="contact.home_phone"
              v-maska="['###-###-####', '###-####-####']"
              type="text"
              maxlength="13"
              placeholder="집전화번호를 선택하세요"
              :disabled="noStatus"
            />
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            기타 연락처
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="contact.other_phone"
              v-maska="['###-###-####', '###-####-####']"
              type="text"
              maxlength="13"
              placeholder="기타 연락처를 입력하세요."
              :disabled="noStatus"
            />
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            이메일
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="contact.email"
              type="email"
              maxlength="50"
              placeholder="이메일 주소를 입력하세요."
              :disabled="noStatus"
            />
          </CCol>
        </CRow>

        <CRow class="mb-0">
          <CAlert
            :color="$store.state.theme === 'dark' ? 'default' : 'secondary'"
            class="pb-0"
          >
            <CRow>
              <CFormLabel class="col-md-2 col-lg-1 col-form-label">
                {{ contLabel }}금
              </CFormLabel>
              <CCol md="10" lg="2" class="mb-3 mb-lg-0">
                <DatePicker
                  placeholder="입금일자"
                  v-maska="'####-##-##'"
                  required
                  :disabled="noStatus"
                />
              </CCol>

              <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

              <CCol md="5" lg="2" class="mb-3 mb-lg-0">
                <CFormInput
                  type="number"
                  min="0"
                  placeholder="입금액"
                  required
                  :disabled="noStatus"
                />
                <CFormFeedback invalid>입금액을 입력하세요.</CFormFeedback>
              </CCol>

              <CCol md="5" lg="2" class="mb-3 mb-lg-0">
                <CFormSelect required :disabled="noStatus">
                  <option value="">납부계좌 선택</option>
                  <option
                    v-for="pb in proBankAccountList"
                    :value="pb.pk"
                    :key="pb.pk"
                  >
                    {{ pb.alias_name }}
                  </option>
                </CFormSelect>
                <CFormFeedback invalid>납부계좌를 선택하세요.</CFormFeedback>
              </CCol>

              <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

              <CCol md="5" lg="2" class="mb-3 mb-lg-0">
                <CFormInput
                  type="text"
                  maxlength="20"
                  placeholder="입금자명을 입력하세요"
                  required
                  :disabled="noStatus"
                />
                <CFormFeedback invalid>입금자명을 입력하세요.</CFormFeedback>
              </CCol>
              <CCol md="5" lg="2" class="mb-md-3 mb-lg-0">
                <CFormSelect required :disabled="noStatus">
                  <option value="">납부회차 선택</option>
                  <option
                    v-for="po in downPayOrder"
                    :value="po.pk"
                    :key="po.pk"
                  >
                    {{ po.__str__ }}
                  </option>
                </CFormSelect>
                <CFormFeedback invalid>납부회차를 선택하세요.</CFormFeedback>
              </CCol>

              <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

              <CCol xs="3" md="2" lg="1" class="pt-2 mb-3 text-center">
                <router-link to="">입금등록</router-link>
              </CCol>
            </CRow>
          </CAlert>
        </CRow>

        <CRow class="mb-0" v-show="isContract">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            주민등록 주소
          </CFormLabel>
          <CCol md="3" lg="2" class="mb-3 mb-lg-0">
            <CInputGroup>
              <CInputGroupText @click="$refs.postCode.initiate(2)">
                우편번호
              </CInputGroupText>
              <CFormInput
                v-model="address.id_zipcode"
                v-maska="'#####'"
                type="text"
                maxlength="5"
                placeholder="우편번호"
                @focus="$refs.postCode.initiate(2)"
                :required="isContract"
                :disabled="!isContract"
              />
              <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>
            </CInputGroup>
          </CCol>

          <CCol md="7" lg="4" class="mb-3 mb-lg-0">
            <CFormInput
              v-model="address.id_address1"
              type="text"
              maxlength="50"
              placeholder="주민등록 주소를 입력하세요"
              @focus="$refs.postCode.initiate(2)"
              :required="isContract"
              :disabled="!isContract"
            />
            <CFormFeedback invalid>주민등록 주소를 입력하세요.</CFormFeedback>
          </CCol>

          <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

          <CCol md="6" lg="2" class="mb-3 mb-lg-0">
            <CFormInput
              v-model="address.id_address2"
              ref="address21"
              type="text"
              maxlength="30"
              placeholder="상세주소를 입력하세요"
              :required="isContract"
              :disabled="!isContract"
            />
            <CFormFeedback invalid>상세주소를 입력하세요.</CFormFeedback>
          </CCol>
          <CCol md="4" lg="2">
            <CFormInput
              v-model="address.id_address3"
              type="text"
              maxlength="30"
              placeholder="참고항목을 입력하세요"
              :disabled="!isContract"
            />
          </CCol>
        </CRow>

        <CRow class="mb-0" v-show="isContract">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            우편수령 주소
          </CFormLabel>
          <CCol md="3" lg="2" class="mb-3 mb-lg-0">
            <CInputGroup>
              <CInputGroupText @click="$refs.postCode.initiate(3)">
                우편번호
              </CInputGroupText>
              <CFormInput
                v-model="address.dm_zipcode"
                v-maska="'#####'"
                type="text"
                maxlength="5"
                placeholder="우편번호"
                @focus="$refs.postCode.initiate(3)"
                :required="isContract"
                :disabled="!isContract"
              />
              <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>
            </CInputGroup>
          </CCol>

          <CCol md="7" lg="4" class="mb-3 mb-lg-0">
            <CFormInput
              v-model="address.dm_address1"
              type="text"
              maxlength="50"
              placeholder="우편물 수령 주소를 입력하세요"
              @focus="$refs.postCode.initiate(3)"
              :required="isContract"
              :disabled="!isContract"
            />
            <CFormFeedback invalid>
              우편물 수령 주소를 입력하세요.
            </CFormFeedback>
          </CCol>

          <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

          <CCol md="6" lg="2" class="mb-3 mb-lg-0">
            <CFormInput
              v-model="address.dm_address2"
              ref="address22"
              type="text"
              maxlength="30"
              placeholder="상세주소를 입력하세요"
              :required="isContract"
              :disabled="!isContract"
            />
            <CFormFeedback invalid>상세주소를 입력하세요.</CFormFeedback>
          </CCol>
          <CCol md="4" lg="2">
            <CFormInput
              v-model="address.dm_address3"
              type="text"
              maxlength="30"
              placeholder="참고항목을 입력하세요"
              :disabled="!isContract"
            />
          </CCol>

          <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

          <CCol md="10" lg="1" class="pt-2 mb-3">
            <CFormCheck
              @click="toSame"
              v-model="sameAddr"
              id="to-same"
              label="상동"
              :disabled="!isContract"
            />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            비고
          </CFormLabel>
          <CCol md="10" lg="11" class="mb-md-3 mb-lg-0">
            <CFormTextarea
              v-model.number="contorForm.note"
              placeholder="기타 특이사항"
              :disabled="noStatus"
            />
          </CCol>
        </CRow>
      </CCardBody>

      <CCardFooter class="text-right">
        <CButton type="button" color="light" @click="formReset"> 취소</CButton>
        <CButton
          type="button"
          v-if="update"
          color="danger"
          @click="deleteProject"
        >
          삭제
        </CButton>
        <CButton type="submit" :color="'primary'" :disabled="formsCheck">
          <CIcon name="cil-check-circle" />
          저장
        </CButton>
      </CCardFooter>
    </CForm>
  </CCard>

  <DaumPostcode @addressPut="addressPut" ref="postCode" />

  <ConfirmModal ref="delModal">
    <template v-slot:header>프로젝트정보 삭제</template>
    <template v-slot:default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template v-slot:footer>
      <CButton color="danger" disabled="">삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>계약 정보 등록</template>
    <template v-slot:default>
      계약 정보 {{ confirmText }}을 진행하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import DatePicker from '@/components/DatePicker/index.vue'
import DaumPostcode from '@/components/DaumPostcode/index.vue'
import addressMixin from '@/components/DaumPostcode/addressMixin'
import { maska } from 'maska'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'IndexForm',
  components: {
    ConfirmModal,
    AlertModal,
    DatePicker,
    DaumPostcode,
  },
  mixins: [addressMixin],
  directives: { maska },
  data() {
    return {
      contPk: null,
      contForm: {
        project: null,
        order_group: '',
        unit_type: '',
        serial_number: '',
        houseunit: '',
        activation: false,
      },
      contorForm: {
        contract: null,
        name: '',
        birth_date: '',
        gender: '',
        is_registed: false,
        status: '',
        cont_date: '',
        reservation_date: '',
        contract_date: '',
        note: '',
      },
      address: {
        contractor: null,
        id_zipcode: '',
        id_address1: '',
        id_address2: '',
        id_address3: '',
        dm_zipcode: '',
        dm_address1: '',
        dm_address2: '',
        dm_address3: '',
      },
      contact: {
        contractor: null,
        cell_phone: '',
        home_phone: '',
        other_phone: '',
        email: '',
      },
      sameAddr: false,
      validated: false,
    }
  },
  props: {
    unitSet: Boolean,
    isUnion: Boolean,
  },
  computed: {
    contLabel() {
      return this.contorForm.status !== '1' ? '계약' : '청약'
    },
    isContract() {
      return this.contorForm.status === '2'
    },
    noStatus() {
      return this.contorForm.status === ''
    },
    downPayOrder() {
      return this.payOrderList.filter((po: any) => po.pay_time <= '1')
    },
    // formsCheck(this: any) {
    //   const a = this.form.name === this.project.name
    //   const b = this.form.order === this.project.order
    //   const c = this.form.kind === this.project.kind
    //
    //   return a && b && c
    // },
    // ...mapGetters('accounts', ['staffAuth', 'superAuth']),
    ...mapState('contract', ['orderGroupList', 'keyUnitList', 'houseUnitList']),
    ...mapState('project', ['unitTypeList']),
    ...mapState('proCash', ['proBankAccountList']),
    ...mapState('payment', ['payOrderList']),
  },
  watch: {
    addrForm(this: any, newVal: number) {
      if (newVal === 2) {
        this.address.id_zipcode = this.zipcode // 우편번호와 주소 정보를 해당 필드에 넣는다.
        this.address.id_address1 = this.address1
        this.address.id_address3 = this.address3 // 조합된 참고항목을 해당 필드에 넣는다.
        this.$refs.address21.$el.focus() // 커서를 상세주소 필드로 이동한다.
      } else if (newVal === 3) {
        this.address.dm_zipcode = this.zipcode // 우편번호와 주소 정보를 해당 필드에 넣는다.
        this.address.dm_address1 = this.address1
        this.address.dm_address3 = this.address3 // 조합된 참고항목을 해당 필드에 넣는다.
        this.$refs.address22.$el.focus() // 커서를 상세주소 필드로 이동한다.
      }
    },
  },
  methods: {
    onSubmit(this: any, event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        console.log(form.checkValidity())
        this.validated = true
      } else this.$refs.confirmModal.callModal()
    },
    unitReset(event: any) {
      if (event.target.value === '') this.formReset()
    },
    typeSelect(event: any) {
      this.$emit('type-select', event.target.value)
      this.contForm.serial_number = ''
      this.contForm.houseunit = ''
    },
    toSame() {
      alert(this.sameAddr)
      this.$nextTick(() => {
        // if (this.sameAddr === true) {
        //   this.address.dm_zipcode = this.address.id_zipcode
        //   this.address.dm_address1 = this.address.id_address1
        //   this.address.dm_address2 = this.address.id_address2
        //   this.address.dm_address3 = this.address.id_address3
        // } else {
        //   this.address.dm_zipcode = ''
        //   this.address.dm_address1 = ''
        //   this.address.dm_address2 = ''
        //   this.address.dm_address3 = ''
        // }
      })
    },
    formReset() {
      this.contForm.project = null
      this.contForm.order_group = ''
      this.contForm.unit_type = ''
      this.contForm.serial_number = ''
      this.contForm.houseunit = ''
      this.contForm.activation = false
      this.contorForm.contract = null
      this.contorForm.name = ''
      this.contorForm.birth_date = ''
      this.contorForm.gender = ''
      this.contorForm.is_registed = false
      this.contorForm.status = ''
      this.contorForm.cont_date = ''
      this.contorForm.reservation_date = ''
      this.contorForm.contract_date = ''
      this.contorForm.note = ''
      this.address.contractor = null
      this.address.id_zipcode = ''
      this.address.id_address1 = ''
      this.address.id_address2 = ''
      this.address.id_address3 = ''
      this.address.dm_zipcode = ''
      this.address.dm_address1 = ''
      this.address.dm_address2 = ''
      this.address.dm_address3 = ''
      this.contact.contractor = null
      this.contact.cell_phone = ''
      this.contact.home_phone = ''
      this.contact.other_phone = ''
      this.contact.email = ''
    },
    modalAction(this: any) {
      const { pk } = this
      this.contorForm.reservation_date = this.dateFormat(
        this.contorForm.reservation_date,
      )
      this.contorForm.cont_date = this.dateFormat(this.contorForm.cont_date)
      this.$emit('on-submit', {
        ...{ pk },
        ...this.contForm,
        ...this.contorForm,
        ...this.address,
        ...this.contact,
      })
      this.validated = false
    },
    // deleteProject(this: any) {
    //   if (this.superAuth) this.$refs.delModal.callModal()
    //   else this.$refs.alertModal.callModal()
    // },
  },
})
</script>
