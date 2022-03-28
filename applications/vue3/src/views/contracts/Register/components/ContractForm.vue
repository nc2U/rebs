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
            <CFormSelect v-model="form.status" @change="unitReset" required>
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
              v-model="form.order_group"
              @change="unitReset"
              required
              :disabled="noStatus"
            >
              <option value="">---------</option>
              <option
                v-for="order in orderGroupList"
                :value="`${order.pk},${order.sort}`"
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
              v-model="form.unit_type"
              @change="typeSelect"
              required
              :disabled="form.order_group === '' && !contract"
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
              v-model="form.key_unit"
              @change="form.houseunit = ''"
              required
              :disabled="form.unit_type === '' && !contract"
            >
              <option value="">---------</option>
              <option
                v-for="unit in keyUnitList"
                :value="`${unit.pk},${unit.unit_code}`"
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
              v-model="form.houseunit"
              :disabled="form.key_unit === '' && !contract"
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
              v-show="form.status === '1'"
              v-model="form.reservation_date"
              v-maska="'####-##-##'"
              placeholder="청약일자"
              :required="form.status === '1'"
              :disabled="noStatus"
            />
            <DatePicker
              v-show="form.status !== '1'"
              v-model="form.contract_date"
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
              v-model="form.name"
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
              v-model="form.birth_date"
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
                v-model="form.gender"
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
                v-model="form.gender"
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
              v-model="form.is_registed"
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
              v-model="form.cell_phone"
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
              v-model="form.home_phone"
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
              v-model="form.other_phone"
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
              v-model="form.email"
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
            <CRow v-if="downPayments.length !== 0" class="mb-3">
              <CCol>
                <CRow
                  v-for="(payment, i) in downPayments"
                  :key="payment.pk"
                  class="text-center mb-1"
                  :class="
                    form.paymentPk === payment.pk
                      ? 'text-success text-decoration-underline'
                      : ''
                  "
                >
                  <CCol>
                    계약금
                    <router-link
                      :to="{
                        name: '건별수납 관리',
                        query: { contract: contract.pk },
                      }"
                      v-c-tooltip="'전체 건별수납 관리'"
                    >
                      납부내역
                    </router-link>
                    [{{ i + 1 }}]
                  </CCol>
                  <CCol class="text-right">{{ payment.deal_date }}</CCol>
                  <CCol class="text-right">
                    <router-link
                      :to="{
                        name: '건별수납 관리',
                        query: { contract: contract.pk },
                      }"
                      v-c-tooltip="'전체 건별수납 관리'"
                    >
                      {{ numFormat(payment.income) }}
                    </router-link>
                  </CCol>
                  <CCol>
                    {{
                      proBankAccountList
                        .filter(b => b.pk === payment.bank_account)
                        .map(b => b.alias_name)[0]
                    }}
                  </CCol>
                  <CCol>{{ payment.trader }}</CCol>
                  <CCol>
                    {{ payment.installment_order.__str__ }}
                  </CCol>
                  <CCol>
                    <CButton
                      type="button"
                      color="success"
                      size="sm"
                      @click="payUpdate(payment)"
                    >
                      수정
                    </CButton>
                  </CCol>
                </CRow>
              </CCol>
            </CRow>
            <CRow>
              <CFormLabel class="col-md-2 col-lg-1 col-form-label">
                {{ contLabel }}금 {{ !form.paymentPk ? '등록' : '수정' }}
              </CFormLabel>
              <CCol md="10" lg="2" class="mb-3 mb-lg-0">
                <DatePicker
                  v-model="form.deal_date"
                  placeholder="입금일자"
                  v-maska="'####-##-##'"
                  :required="!contract"
                  :disabled="noStatus"
                />
              </CCol>

              <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

              <CCol md="5" lg="2" class="mb-3 mb-lg-0">
                <CFormInput
                  v-model="form.income"
                  type="number"
                  min="0"
                  placeholder="입금액"
                  :required="!contract"
                  :disabled="noStatus"
                />
                <CFormFeedback invalid>입금액을 입력하세요.</CFormFeedback>
              </CCol>

              <CCol md="5" lg="2" class="mb-3 mb-lg-0">
                <CFormSelect
                  v-model="form.bank_account"
                  :required="!contract"
                  :disabled="noStatus"
                >
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
                  v-model="form.trader"
                  maxlength="20"
                  placeholder="입금자명을 입력하세요"
                  :required="!contract"
                  :disabled="noStatus"
                />
                <CFormFeedback invalid>입금자명을 입력하세요.</CFormFeedback>
              </CCol>
              <CCol md="5" lg="2" class="mb-md-3 mb-lg-0">
                <CFormSelect
                  v-model="form.installment_order"
                  :required="!contract"
                  :disabled="noStatus"
                >
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

              <CCol
                v-if="form.paymentPk"
                xs="3"
                md="2"
                lg="1"
                class="pt-2 mb-3"
              >
                <router-link to="" @click="payReset">Reset</router-link>
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
                v-model="form.id_zipcode"
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
              v-model="form.id_address1"
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
              v-model="form.id_address2"
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
              v-model="form.id_address3"
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
                v-model="form.dm_zipcode"
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
              v-model="form.dm_address1"
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
              v-model="form.dm_address2"
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
              v-model="form.dm_address3"
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
              :disabled="!isContract || !form.id_zipcode"
            />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            비고
          </CFormLabel>
          <CCol md="10" lg="11" class="mb-md-3 mb-lg-0">
            <CFormTextarea
              v-model.number="form.note"
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
          v-if="contract"
          color="danger"
          @click="deleteContract"
        >
          삭제
        </CButton>
        <CButton
          type="submit"
          :color="contract ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
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
    <template v-slot:header>
      <CIcon name="cilItalic" />
      {{ contLabel }} 정보 등록
    </template>
    <template v-slot:default>
      {{ contLabel }} 정보 {{ contract ? '수정등록' : '신규등록' }}을
      진행하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton
        :color="contract ? 'success' : 'primary'"
        @click="modalAction"
        :disabled="formsCheck"
      >
        저장
      </CButton>
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
import { mapGetters, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractForm',
  components: {
    ConfirmModal,
    AlertModal,
    DatePicker,
    DaumPostcode,
  },
  mixins: [addressMixin],
  directives: { maska },
  props: {
    contract: Object,
    unitSet: Boolean,
    isUnion: Boolean,
  },
  data() {
    return {
      pk: null,
      form: {
        // contract
        order_group: '', // 2
        unit_type: '', // 3
        key_unit: '', // 4
        houseunit: '', // 5
        cont_keyunit: '', // 디비 계약 유닛
        cont_houseunit: '', // 디비 동호 유닛
        // contractor
        contractorPk: null,
        name: '', // 7
        birth_date: null, // 8
        gender: '', // 9
        is_registed: false, // 10
        status: '', // 1
        reservation_date: null, // 6-1
        contract_date: null, // 6-2
        note: '', // 28
        // proCash
        paymentPk: null,
        deal_date: null, // 15
        income: '', // 16
        bank_account: '', // 17
        trader: '', // 18
        installment_order: '', // 19
        // address
        addressPk: null,
        id_zipcode: '', // 20
        id_address1: '', // 21
        id_address2: '', // 22
        id_address3: '', // 23
        dm_zipcode: '', // 24
        dm_address1: '', // 25
        dm_address2: '', // 26
        dm_address3: '', // 27
        // contact
        contactPk: null,
        cell_phone: '', // 11
        home_phone: '', // 12
        other_phone: '', // 13
        email: '', // 14
      },
      sameAddr: false,
      formsCheck: true,
      validated: false,
    }
  },
  computed: {
    contLabel() {
      return this.form.status !== '1' ? '계약' : '청약'
    },
    isContract() {
      return this.form.status === '2'
    },
    noStatus() {
      return this.form.status === '' && !this.contract
    },
    downPayOrder() {
      return this.payOrderList.filter((po: any) => po.pay_time <= '1')
    },
    downPayments(this: any) {
      return this.contract && this.contract.payments.length > 0
        ? this.contract.payments.filter(
            (p: any) =>
              p.installment_order !== null &&
              p.installment_order.pay_time === 1,
          )
        : []
    },
    pageManageAuth() {
      return (
        this.superAuth || (this.staffAuth && this.staffAuth.contract === '2')
      )
    },
    allowedPeriod(this: any) {
      return (
        this.superAuth ||
        this.form.paymentPk === null ||
        this.diffDate(this.form.deal_date) <= 90
      )
    },
    ...mapState('contract', ['orderGroupList', 'keyUnitList', 'houseUnitList']),
    ...mapState('project', ['unitTypeList']),
    ...mapState('proCash', ['proBankAccountList']),
    ...mapState('payment', ['payOrderList']),
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  watch: {
    addrForm(this: any, newVal: number) {
      if (newVal === 2) {
        this.form.id_zipcode = this.zipcode // 우편번호와 주소 정보를 해당 필드에 넣는다.
        this.form.id_address1 = this.address1
        this.form.id_address3 = this.address3 // 조합된 참고항목을 해당 필드에 넣는다.
        this.$refs.address21.$el.focus() // 커서를 상세주소 필드로 이동한다.
      } else if (newVal === 3) {
        this.form.dm_zipcode = this.zipcode // 우편번호와 주소 정보를 해당 필드에 넣는다.
        this.form.dm_address1 = this.address1
        this.form.dm_address3 = this.address3 // 조합된 참고항목을 해당 필드에 넣는다.
        this.$refs.address22.$el.focus() // 커서를 상세주소 필드로 이동한다.
      }
    },
    contract(this: any, newVal) {
      if (this.contract && newVal) {
        // contract
        this.pk = this.contract.pk
        this.form.order_group = `${this.contract.order_group.pk},${this.contract.order_group.sort}`
        this.form.unit_type = this.contract.unit_type.pk
        this.form.key_unit = `${this.contract.keyunit.pk},${this.contract.keyunit.unit_code}`
        this.form.houseunit = this.contract.keyunit.houseunit
          ? this.contract.keyunit.houseunit.pk
          : ''
        this.form.cont_keyunit = this.contract.keyunit.pk
        this.form.cont_houseunit = this.contract.keyunit.houseunit
          ? this.contract.keyunit.houseunit.pk
          : ''

        // contractor
        this.form.contractorPk = this.contract.contractor.pk
        this.form.name = this.contract.contractor.name
        this.form.birth_date = new Date(this.contract.contractor.birth_date)
        this.form.gender = this.contract.contractor.gender // 9
        this.form.is_registed = this.contract.contractor.is_registed // 10
        this.form.status = this.contract.contractor.status
        this.form.reservation_date =
          this.contract.contractor.reservation_date === null
            ? null
            : new Date(this.contract.contractor.reservation_date)
        this.form.contract_date =
          this.contract.contractor.contract_date === null
            ? null
            : new Date(this.contract.contractor.contract_date)
        this.form.note = this.contract.contractor.note

        // address
        if (newVal.contractor.status === '2') {
          this.form.addressPk = this.contract.contractor.contractoraddress.pk
          this.form.id_zipcode =
            this.contract.contractor.contractoraddress.id_zipcode // 20
          this.form.id_address1 =
            this.contract.contractor.contractoraddress.id_address1 // 21
          this.form.id_address2 =
            this.contract.contractor.contractoraddress.id_address2 // 22
          this.form.id_address3 =
            this.contract.contractor.contractoraddress.id_address3 // 23
          this.form.dm_zipcode =
            this.contract.contractor.contractoraddress.dm_zipcode // 24
          this.form.dm_address1 =
            this.contract.contractor.contractoraddress.dm_address1
          this.form.dm_address2 =
            this.contract.contractor.contractoraddress.dm_address2 // 26
          this.form.dm_address3 =
            this.contract.contractor.contractoraddress.dm_address3 // 27
        }
        // contact
        this.form.contactPk = this.contract.contractor.contractorcontact.pk //
        this.form.cell_phone =
          this.contract.contractor.contractorcontact.cell_phone
        this.form.home_phone =
          this.contract.contractor.contractorcontact.home_phone // 11 // 12
        this.form.other_phone =
          this.contract.contractor.contractorcontact.other_phone // 13
        this.form.email = this.contract.contractor.contractorcontact.email // 14
      }
      this.$nextTick(() => (this.formsCheck = true))
    },
    form: {
      deep: true,
      handler() {
        this.formsCheck = false
      },
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
      } else {
        if (this.pageManageAuth)
          if (this.allowedPeriod) this.$refs.confirmModal.callModal()
          else
            this.$refs.alertModal.callModal(
              null,
              '거래일로부터 90일이 경과한 건은 수정할 수 없습니다. 관리자에게 문의바랍니다.',
            )
        else this.$refs.alertModal.callModal()
      }
    },
    payUpdate(this: any, payment: any) {
      this.form.paymentPk = payment.pk
      this.form.deal_date = new Date(payment.deal_date)
      this.form.income = payment.income
      this.form.bank_account = payment.bank_account
      this.form.trader = payment.trader
      this.form.installment_order = payment.installment_order.pk
    },
    payReset() {
      this.form.paymentPk = null
      this.form.deal_date = null
      this.form.income = ''
      this.form.bank_account = ''
      this.form.trader = ''
      this.form.installment_order = ''
    },
    unitReset(event: any) {
      this.form.reservation_date = null
      this.form.contract_date = null
      if (event.target.value === '') this.formReset()
    },
    typeSelect(event: any) {
      this.$emit('type-select', event.target.value)
      this.form.key_unit = ''
      this.form.houseunit = ''
    },
    toSame() {
      if (!this.sameAddr) {
        this.form.dm_zipcode = this.form.id_zipcode
        this.form.dm_address1 = this.form.id_address1
        this.form.dm_address2 = this.form.id_address2
        this.form.dm_address3 = this.form.id_address3
      } else {
        this.form.dm_zipcode = ''
        this.form.dm_address1 = ''
        this.form.dm_address2 = ''
        this.form.dm_address3 = ''
      }
    },
    formReset() {
      this.pk = null
      this.form.order_group = ''
      this.form.unit_type = ''
      this.form.key_unit = ''
      this.form.houseunit = ''

      this.form.contractorPk = null
      this.form.name = ''
      this.form.birth_date = null
      this.form.gender = ''
      this.form.is_registed = false
      this.form.status = ''
      this.form.reservation_date = null
      this.form.contract_date = null
      this.form.note = ''

      this.form.paymentPk = null
      this.form.deal_date = null
      this.form.income = ''
      this.form.bank_account = ''
      this.form.trader = ''
      this.form.installment_order = ''

      this.form.addressPk = null
      this.form.id_zipcode = ''
      this.form.id_address1 = ''
      this.form.id_address2 = ''
      this.form.id_address3 = ''
      this.form.dm_zipcode = ''
      this.form.dm_address1 = ''
      this.form.dm_address2 = ''
      this.form.dm_address3 = ''

      this.form.contactPk = null
      this.form.cell_phone = ''
      this.form.home_phone = ''
      this.form.other_phone = ''
      this.form.email = ''
      this.FETCH_CONTRACT(null)
      this.$router.push({ name: '계약등록 관리' })
      this.$nextTick(() => (this.formsCheck = true))
    },
    modalAction(this: any) {
      this.form.birth_date = this.form.birth_date
        ? this.dateFormat(this.form.birth_date)
        : null
      this.form.reservation_date = this.form.reservation_date
        ? this.dateFormat(this.form.reservation_date)
        : null
      this.form.contract_date = this.form.contract_date
        ? this.dateFormat(this.form.contract_date)
        : null
      this.form.deal_date = this.form.deal_date
        ? this.dateFormat(this.form.deal_date)
        : null
      if (!this.contract) this.$emit('on-create', this.form)
      else
        this.$emit('on-update', {
          ...{ pk: this.pk },
          ...this.form,
        })
      this.validated = false
      this.formReset()
      this.$refs.confirmModal.visible = false
    },
    deleteContract(this: any) {
      if (this.superAuth) this.$refs.delModal.callModal()
      else this.$refs.alertModal.callModal()
    },
    ...mapMutations('contract', ['FETCH_CONTRACT']),
  },
})
</script>
