<template>
  <CCard>
    <CCardHeader>
      <CIcon name="cil-notes" />
      <strong class="pl-1"> 프로젝트 정보 {{ confirmText }} </strong>
    </CCardHeader>

    <CForm
      class="needs-validation"
      novalidate
      :validated="validated"
      @submit.prevent="onSubmit"
    >
      <CCardBody>
        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 프로젝트명</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.name"
              type="text"
              maxlength="30"
              placeholder="프로젝트명을 입력하세요"
              required
            />
            <CFormFeedback invalid>프로젝트명을 입력하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 정렬순서</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.order"
              type="number"
              min="0"
              placeholder="프로젝트 정력순서를 입력하세요"
            />
            <CFormFeedback invalid>정렬순서를 입력하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 프로젝트종류</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormSelect v-model="form.kind" required>
              <option value="">프로젝트 종류</option>
              <option
                v-for="sort in sortOptins"
                :value="sort.value"
                :key="sort.value"
                :selected="update && sort.value === project.kind"
              >
                {{ sort.label }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>프로젝트종류를 선택하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 사업개시년도</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.start_year"
              type="number"
              min="1990"
              placeholder="사업개시년도를 입력하세요"
              required
            />
            <CFormFeedback invalid>
              사업개시년도를 입력하세요(1990년도 이후).
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 직영운영여부</CFormLabel>
          <CCol md="8" lg="5">
            <CFormSwitch
              v-model="form.is_direct_manage"
              :checked="update && project.is_direct_manage"
            />
          </CCol>
          <CFormText class="text-secondary">
            본사 직접 운영하는 프로젝트인 경우 체크, 즉 시행대행이나 업무대행이
            아닌 경우
          </CFormText>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 토지환지여부</CFormLabel>
          <CCol md="8" lg="5">
            <CFormSwitch
              v-model="form.is_returned_area"
              :checked="update && project.is_returned_area"
            />
          </CCol>
          <CFormText class="text-secondary">
            해당 사업부지가 환지방식 도시개발사업구역인 경우 체크
          </CFormText>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 동호지정여부</CFormLabel>
          <CCol md="8" lg="5">
            <CFormSwitch
              v-model="form.is_unit_set"
              :checked="update && project.is_unit_set"
            />
          </CCol>
          <CFormText class="text-secondary">
            현재 동호수를 지정하지 않는 경우 체크하지 않음
          </CFormText>
        </CRow>
        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 우편번호</CFormLabel>
          <CCol md="3" lg="2" class="mb-3 mb-lg-0">
            <CInputGroup>
              <CInputGroupText @click="$refs.postCode.initiate()">
                우편번호
              </CInputGroupText>
              <CFormInput
                v-model="form.local_zipcode"
                type="text"
                maxlength="5"
                placeholder="우편번호"
                @focus="$refs.postCode.initiate()"
              />
              <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>
            </CInputGroup>
          </CCol>

          <CCol md="7" lg="4" class="mb-3 mb-lg-0">
            <CFormInput
              v-model="form.local_address1"
              type="text"
              maxlength="50"
              placeholder="대표지번 주소를 입력하세요"
              @focus="$refs.postCode.initiate()"
            />
            <CFormFeedback invalid>대표지번 주소를 입력하세요.</CFormFeedback>
          </CCol>

          <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

          <CCol md="5" lg="2" class="mb-3 mb-lg-0">
            <CFormInput
              v-model="form.local_address2"
              ref="address2"
              type="text"
              maxlength="25"
              placeholder="상세주소를 입력하세요"
            />
            <CFormFeedback invalid>상세주소를 입력하세요.</CFormFeedback>
          </CCol>
          <CCol md="5" lg="2">
            <CFormInput
              v-model="form.local_address3"
              type="text"
              maxlength="20"
              placeholder="참고항목을 입력하세요"
            />
            <CFormFeedback invalid>참고항목을 입력하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 용도지역지구</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.area_usage"
              type="text"
              maxlength="50"
              placeholder="용도지역지구를 입력하세요"
              required
            />
            <CFormFeedback invalid>용도지역지구를 입력하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 건축규모</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.build_size"
              type="text"
              maxlength="50"
              placeholder="건축규모를 입력하세요"
              required
            />
            <CFormFeedback invalid>건축규모를 입력하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label">
            세대(호/실)수
          </CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.num_unit"
              type="number"
              min="0"
              placeholder="세대(호/실)수를 입력하세요"
            />
            <CFormFeedback invalid>세대(호/실)수를 입력하세요.</CFormFeedback>
          </CCol>
          <CFormLabel class="col-md-2 col-form-label"> 대지매입면적</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.buy_land_extent"
              type="number"
              min="0"
              step="0.0001"
              placeholder="대지매입면적을 입력하세요"
            />
            <CFormFeedback invalid>
              대지매입면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 계획대지면적</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.scheme_land_extent"
              type="number"
              min="0"
              step="0.0001"
              placeholder="계획대지면적을 입력하세요"
            />
            <CFormFeedback invalid>
              계획대지면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 기부채납면적</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.donation_land_extent"
              type="number"
              min="0"
              step="0.0001"
              placeholder="기부채납면적을 입력하세요"
            />
            <CFormFeedback invalid>
              기부채납면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 지상연면적</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.on_floor_area"
              type="number"
              min="0"
              step="0.0001"
              placeholder="지상연면적을 입력하세요"
            />
            <CFormFeedback invalid>
              지상연면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 지하연면적</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.under_floor_area"
              type="number"
              min="0"
              step="0.0001"
              placeholder="지하연면적을 입력하세요"
            />
            <CFormFeedback invalid>
              지하연면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 총 연면적</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.total_floor_area"
              type="number"
              min="0"
              step="0.0001"
              placeholder="총 연면적을 입력하세요"
            />
            <CFormFeedback invalid>
              총 연면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 건축면적</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.build_area"
              type="number"
              min="0"
              step="0.0001"
              placeholder="건축면적을 입력하세요"
            />
            <CFormFeedback invalid>
              총 연면적을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 용적율(%)</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.floor_area_ratio"
              type="number"
              min="0"
              step="0.0001"
              placeholder="용적율(%)을 입력하세요"
            />
            <CFormFeedback invalid>
              용적율(%)을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
          <CFormLabel class="col-md-2 col-form-label"> 건폐율(%)</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.build_to_land_ratio"
              type="number"
              min="0"
              step="0.0001"
              placeholder="건폐율(%)을 입력하세요"
            />
            <CFormFeedback invalid>
              건폐율(%)을 소소점4자리 이하로 입력하세요.
            </CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-form-label"> 법정주차대수</CFormLabel>
          <CCol md="10" lg="4" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.num_legal_parking"
              type="number"
              min="0"
              placeholder="법정주차대수를 입력하세요"
            />
            <CFormFeedback invalid>법정주차대수를 입력하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-form-label"> 계획주차대수</CFormLabel>
          <CCol md="10" lg="4">
            <CFormInput
              v-model="form.num_planed_parking"
              type="number"
              min="0"
              placeholder="계획주차대수를 입력하세요"
            />
            <CFormFeedback invalid>계획주차대수를 입력하세요.</CFormFeedback>
          </CCol>
        </CRow>
      </CCardBody>

      <CCardFooter class="text-right">
        <CButton type="button" color="light" @click="this.$emit('reset-form')">
          취소
        </CButton>
        <CButton
          v-if="update && superAuth"
          type="button"
          color="danger"
          @click="deleteCompany"
        >
          삭제
        </CButton>
        <CButton v-if="staffAuth" type="submit" :color="btnClass">
          <CIcon name="cil-check-circle" />
          저장
        </CButton>
      </CCardFooter>
    </CForm>

    <DaumPostcode @addressPut="addressPut" ref="postCode" />

    <ConfirmModal ref="delModal">
      <template v-slot:header>프로젝트정보 삭제</template>
      <template v-slot:default>현재 삭제 기능이 구현되지 않았습니다.</template>
      <template v-slot:footer>
        <CButton color="danger" disabled="">삭제</CButton>
      </template>
    </ConfirmModal>

    <ConfirmModal ref="confirmModal">
      <template v-slot:header>프로젝트정보</template>
      <template v-slot:default>
        프로젝트정보 {{ confirmText }}을 진행하시겠습니까?
      </template>
      <template v-slot:footer>
        <CButton :color="btnClass" @click="modalAction">저장</CButton>
      </template>
    </ConfirmModal>
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import DaumPostcode from '@/components/DaumPostcode/index.vue'
import addressMixin from '@/components/DaumPostcode/addressMixin'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'IndexForm',
  components: { ConfirmModal, DaumPostcode },
  mixins: [addressMixin],
  data() {
    return {
      pk: null,
      form: {
        name: '',
        order: null,
        kind: '',
        start_year: '',
        is_direct_manage: false,
        is_returned_area: false,
        is_unit_set: false,
        local_zipcode: '',
        local_address1: '',
        local_address2: '',
        local_address3: '',
        area_usage: '',
        build_size: '',
        num_unit: null,
        buy_land_extent: null,
        scheme_land_extent: null,
        donation_land_extent: null,
        on_floor_area: null,
        under_floor_area: null,
        total_floor_area: null,
        build_area: null,
        floor_area_ratio: null,
        build_to_land_ratio: null,
        num_legal_parking: null,
        num_planed_parking: null,
      },
      sortOptins: [
        { value: '1', label: '공동주택(아파트)' },
        { value: '2', label: '공동주택(타운하우스)' },
        { value: '3', label: '주상복합(아파트)' },
        { value: '4', label: '주상복합(오피스텔)' },
        { value: '5', label: '근린생활시설' },
        { value: '6', label: '생활형숙박시설' },
        { value: '7', label: '지식산업센터' },
        { value: '8', label: '기타' },
      ],
      validated: false,
    }
  },
  created() {
    if (this.update && this.project) {
      this.pk = this.project.pk
      this.form.name = this.project.name
      this.form.order = this.project.order
      this.form.kind = this.project.kind
      this.form.start_year = this.project.start_year
      this.form.is_direct_manage = this.project.is_direct_manage
      this.form.is_returned_area = this.project.is_returned_area
      this.form.is_unit_set = this.project.is_unit_set
      this.form.local_zipcode = this.project.local_zipcode
      this.form.local_address1 = this.project.local_address1
      this.form.local_address2 = this.project.local_address2
      this.form.local_address3 = this.project.local_address3
      this.form.area_usage = this.project.area_usage
      this.form.build_size = this.project.build_size
      this.form.num_unit = this.project.num_unit
      this.form.buy_land_extent = this.project.buy_land_extent
      this.form.scheme_land_extent = this.project.scheme_land_extent
      this.form.donation_land_extent = this.project.donation_land_extent
      this.form.on_floor_area = this.project.on_floor_area
      this.form.under_floor_area = this.project.under_floor_area
      this.form.total_floor_area = this.project.total_floor_area
      this.form.build_area = this.project.build_area
      this.form.floor_area_ratio = this.project.floor_area_ratio
      this.form.build_to_land_ratio = this.project.build_to_land_ratio
      this.form.num_legal_parking = this.project.num_legal_parking
      this.form.num_planed_parking = this.project.num_planed_parking
    }
  },
  props: {
    userInfo: {
      type: Object,
    },
    project: {
      type: Object,
    },
    update: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    company() {
      return this.update
        ? (this as any).project.company
        : (this as any).userInfo.staffauth.company
    },
    confirmText() {
      return this.update ? '변경' : '등록'
    },
    btnClass() {
      return this.update ? 'success' : 'primary'
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  watch: {
    zipcode(value) {
      this.form.local_zipcode = value
    },
    address1(value) {
      this.form.local_address1 = value
    },
    address3(value) {
      this.form.local_address3 = value
    },
  },
  methods: {
    onSubmit(event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        console.log(form.checkValidity())
        this.validated = true
      } else {
        ;(this as any).$refs.confirmModal.callModal()
      }
    },
    modalAction() {
      const { pk, company } = this
      if (this.update) {
        this.$emit('to-update', { ...{ pk, company }, ...this.form })
      } else {
        this.$emit('to-create', { ...{ company }, ...this.form })
      }
      this.validated = false
    },
    deleteCompany() {
      ;(this as any).$refs.delModal.callModal()
    },
  },
})
</script>

<style lang="scss" scoped></style>
