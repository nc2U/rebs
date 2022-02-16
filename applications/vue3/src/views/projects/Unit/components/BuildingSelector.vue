<template>
  <CCallout color="info" class="pb-2">
    <CRow>
      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label">
            동(건물)선택
          </CFormLabel>
          <CCol sm="8">
            <CFormSelect
              v-model="building"
              @change="bldgSelect"
              :disabled="!project"
            >
              <option value>---------</option>
              <option
                v-for="building in buildingList"
                :key="building.pk"
                :value="building.pk"
              >
                {{ building.name }}동
              </option>
            </CFormSelect>
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
            <CFormSelect v-model="type" :disabled="building == ''">
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
            <CFormInput
              v-model.number="line"
              type="number"
              min="0"
              placeholder="등록할 라인 숫자 입력"
              :disabled="type == ''"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 최저층</CFormLabel>
          <CCol sm="8">
            <CFormInput
              v-model.number="minFloor"
              type="number"
              placeholder="최저층(피로티 제외)"
              :disabled="line == ''"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 최고층</CFormLabel>
          <CCol sm="8">
            <CFormInput
              v-model.number="maxFloor"
              type="number"
              min="0"
              placeholder="해당 라인 최고층"
              :disabled="minFloor == ''"
            />
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>

  <CAlert color="secondary" class="text-right">
    <CButton color="primary">호수등록</CButton>
  </CAlert>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'BuildingSelector',
  components: {},
  props: ['project'],
  data() {
    return {
      building: '',
      type: '',
      line: '',
      minFloor: '',
      maxFloor: '',
    }
  },
  computed: {
    ...mapState('project', ['unitTypeList', 'buildingList']),
  },
  watch: {
    project() {
      this.building = ''
    },
    building(val) {
      if (val == '') this.reset(1)
    },
    type(val) {
      if (val == '') this.reset(2)
    },
    line(val) {
      if (val == '') this.reset(3)
    },
    minFloor(val) {
      if (val == '') this.reset(4)
    },
  },
  methods: {
    reset(n: number): void {
      if (n == 1) {
        this.type = ''
        this.line = ''
        this.minFloor = ''
        this.maxFloor = ''
      } else if (n == 2) {
        this.line = ''
        this.minFloor = ''
        this.maxFloor = ''
      } else if (n == 3) {
        this.minFloor = ''
        this.maxFloor = ''
      } else {
        this.maxFloor = ''
      }
    },
    bldgSelect(this: any, event: any) {
      this.$emit('bldg-select', event.target.value)
    },
  },
})
</script>
