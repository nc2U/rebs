<template>
  <CCallout color="primary" class="pb-0 mb-4">
    <CRow>
      <CCol lg="8">
        <CRow>
          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.limit">
              <option value="">표시 개수</option>
              <option value="5">5 개</option>
              <option value="10">10 개</option>
              <option value="15">15 개</option>
              <option value="20">20 개</option>
              <option value="25">25 개</option>
              <option value="30">30 개</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.group">
              <option value="">차수선택</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.type">
              <option value="">타입선택</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.dong">
              <option value="">동 선택</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.order">
              <option value="-created_at">등록일시 내림차순</option>
              <option value="created_at">등록일시 올림차순</option>
              <option value="-contractor__contract_date">
                계약일자 내림차순
              </option>
              <option value="contractor__contract_date">
                계약일자 올림차순
              </option>
              <option value="-serial_number">일련번호 내림차순</option>
              <option value="serial_number">일련번호 올림차순</option>
              <option value="-contractor__name">계약자명 내림차순</option>
              <option value="contractor__name">계약자명 올림차순</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="2">
        <CRow>
          <CCol md="12" class="mb-3"> aaa</CCol>
        </CRow>
      </CCol>

      <CCol lg="2">
        <CRow>
          <CCol class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.q"
                placeholder="계약자, 일련번호, 비고"
                aria-label="Username"
                aria-describedby="addon-wrapping"
              />
              <CInputGroupText @click="listFiltering(1)">검색</CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <CRow>
      <CCol color="warning" class="p-2 pl-3">
        <strong>계약 건수 조회 결과 : 11건</strong>
      </CCol>
      <CCol class="text-right mb-0">
        <CButton color="info" size="sm"> 검색조건 초기화</CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { maska } from 'maska'

export default defineComponent({
  name: 'ListController',
  directives: { maska },
  components: {},
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      form: {
        limit: '',
        group: '',
        type: '',
        dong: '',
        order: '',
        q: '',
      },
    }
  },
  computed: {},
  methods: {},
})
</script>
