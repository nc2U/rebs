<template>
  <CCallout color="success" class="pb-0 mb-4">
    <CRow>
      <CCol md="9">
        <CRow>
          <CCol md="2">
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

          <CCol md="2">
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

          <CCol md="2">
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
          <CCol md="2">
            <CFormSelect id="inputState">
              <option>계약 상태</option>
              <option value="3">해지 신청</option>
            </CFormSelect>
          </CCol>
          <CCol md="2" class="mb-3">
            <CFormInput
              type="text"
              id="inputEmail4"
              placeholder="계약 기간 : From"
            />
          </CCol>
          <CCol md="2">
            <CFormInput id="inputZip" placeholder="계약 기간 : To" />
          </CCol>
        </CRow>
      </CCol>
      <CCol md="3">
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
    <CAlert color="secondary" />
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ListController',
  components: {},
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
