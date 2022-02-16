<template>
  <CCallout color="info" class="pb-2">
    <CRow>
      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label">
            동(건물)선택
          </CFormLabel>
          <CCol sm="8">
            <CFormSelect v-model="building" :disabled="disabled">
              <option value>---------</option>
              <option v-for="building in buildingList" :key="building.pk">
                {{ building.name }}동
              </option>
            </CFormSelect>
            <!--            <CFormText>입력할 동을 선택하여 주세요.</CFormText>-->
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>

  <CCallout color="danger" class="pb-2">
    <CRow>
      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 타입선택</CFormLabel>
          <CCol sm="8">
            <CFormSelect v-model="type" :disabled="disabled">
              <option value>---------</option>
              <option v-for="type in unitTypeList" :key="type.pk">
                {{ type.name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 등록라인</CFormLabel>
          <CCol sm="8">
            <CFormInput type="number" placeholder="등록할 라인 숫자 입력" />
          </CCol>
        </CRow>
      </CCol>

      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 최저층</CFormLabel>
          <CCol sm="8">
            <CFormInput type="number" placeholder="최저층(피로티 제외)" />
          </CCol>
        </CRow>
      </CCol>

      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 최고층</CFormLabel>
          <CCol sm="8">
            <CFormInput type="number" placeholder="해당 라인 최고층" />
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>

  <CAlert color="secondary">
    <CButton color="primary">호수등록</CButton>
  </CAlert>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'BuildingSelector',
  components: {},

  data() {
    return {
      type: '',
      building: '',
      disabled: false,
    }
  },
  computed: {
    ...mapState('project', ['unitTypeList', 'buildingList']),
  },
  methods: {
    onBuildingSelect(e: any) {
      this.$emit('on-select', e.target.value)
    },
  },
})
</script>
