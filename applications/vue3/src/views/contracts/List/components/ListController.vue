<template>
  <CCallout color="success" class="pb-0 mb-4">
    <CRow>
      <CCol lg="7">
        <CRow>
          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect id="inputState">
              <option value="1">계약 현황</option>
              <option value="2">청약 현황</option>
              <option value="3">해지 신청</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect id="inputState">
              <option>차수선택</option>
              <option
                v-for="order in orderGroupList"
                :value="order.pk"
                :key="order.pk"
              >
                {{ order.order_group_name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect id="inputState">
              <option>타입선택</option>
              <option
                v-for="type in simpleTypes"
                :value="type.pk"
                :key="type.pk"
              >
                {{ type.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect id="inputState">
              <option>동 선택</option>
              <option
                v-for="bldg in buildingList"
                :value="bldg.pk"
                :key="bldg.pk"
              >
                {{ bldg.name }}동
              </option>
            </CFormSelect>
          </CCol>
          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect id="inputState">
              <option value="">인가 구분</option>
              <option value="1">인가</option>
              <option value="2">미인가</option>
            </CFormSelect>
          </CCol>
          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect id="inputState">
              <option value="1">등록일시 내림차순</option>
              <option value="2">등록일시 올림차순</option>
              <option value="3">계약일자 내림차순</option>
              <option value="4">계약일자 올림차순</option>
              <option value="5">일련번호 내림차순</option>
              <option value="6">일련번호 올림차순</option>
              <option value="7">계약자명 내림차순</option>
              <option value="8">계약자명 올림차순</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
      <CCol lg="5">
        <CRow>
          <CCol md="6" lg="3" class="mb-3">
            <CFormInput v-maska="'####-##-##'" placeholder="계약일자(From)" />
          </CCol>
          <CCol md="6" lg="3" class="mb-3">
            <CFormInput v-maska="'####-##-##'" placeholder="계약일자(To)" />
          </CCol>
          <CCol lg="6" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                placeholder="계약자, 일련번호, 비고"
                aria-label="Username"
                aria-describedby="addon-wrapping"
              />
              <CInputGroupText id="addon-wrapping">검색</CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <!--    <CAlert color="secondary" />-->
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters, mapState } from 'vuex'
import { maska } from 'maska'

export default defineComponent({
  name: 'ListController',
  directives: { maska },
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {
    ...mapState('contract', ['orderGroupList']),
    ...mapState('project', ['buildingList']),
    ...mapGetters('project', ['simpleTypes']),
  },
  methods: {},
})
</script>
