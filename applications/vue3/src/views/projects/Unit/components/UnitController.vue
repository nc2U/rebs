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
              v-model="form.building"
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
            <CFormSelect v-model="form.type" :disabled="form.building == ''">
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
              v-model.number="form.line"
              type="number"
              min="0"
              placeholder="등록할 라인 숫자 입력"
              :disabled="form.type == ''"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 최저층</CFormLabel>
          <CCol sm="8">
            <CFormInput
              v-model.number="form.minFloor"
              type="number"
              placeholder="최저층(피로티 제외)"
              :disabled="form.line == ''"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 최고층</CFormLabel>
          <CCol sm="8">
            <CFormInput
              v-model.number="form.maxFloor"
              type="number"
              min="0"
              placeholder="해당 라인 최고층"
              :disabled="form.minFloor == ''"
            />
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>

  <CAlert color="danger" v-if="warning">
    <CIcon name="cilWarning" />
    <strong> 주의</strong> : 해당 라인의 최저층부터 최고층까지 범위의
    호수(유니트)가 일괄등록됩니다. 해당 동, 타입과 층을 다시한번 확인하고
    신중하게 진행하십시요.
  </CAlert>

  <CAlert color="secondary" class="text-right">
    <CButton
      color="primary"
      @click="unitRegister"
      :disabled="form.minFloor === ''"
    >
      호수(유니트) 일괄등록
    </CButton>
  </CAlert>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cilItalic" />
      호수(유니트) 정보
    </template>
    <template v-slot:default>
      <p class="text-primary">
        <strong>
          {{ form.building }}동({{ form.type }} 타입 - {{ form.line }}호 라인)
          최저층 : {{ form.minFloor }} - 최고층 : {{ form.maxFloor }}
        </strong>
      </p>
      <p>상기 호수(유니트)정보의 일괄등록을 진행하시겠습니까?</p>
    </template>
    <template v-slot:footer>
      <CButton color="primary" @click="modalAction">일괄등록</CButton>
    </template>
  </ConfirmModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'BuildingSelector',
  components: { ConfirmModal },
  props: ['project'],
  data() {
    return {
      form: {
        building: '',
        type: '',
        line: '',
        minFloor: '',
        maxFloor: '',
      },
    }
  },
  computed: {
    warning() {
      return this.form.maxFloor !== ''
    },
    ...mapState('project', ['unitTypeList', 'buildingList']),
  },
  watch: {
    project() {
      this.form.building = ''
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
        this.form.type = ''
        this.form.line = ''
        this.form.minFloor = ''
        this.form.maxFloor = ''
      } else if (n == 2) {
        this.form.line = ''
        this.form.minFloor = ''
        this.form.maxFloor = ''
      } else if (n == 3) {
        this.form.minFloor = ''
        this.form.maxFloor = ''
      } else {
        this.form.maxFloor = ''
      }
    },
    bldgSelect(this: any, event: any) {
      this.$emit('bldg-select', event.target.value)
    },
    unitRegister(this: any) {
      this.$refs.confirmModal.callModal()
    },
    modalAction(this: any) {
      this.$emit('unit-register', this.form)
      this.$refs.confirmModal.visible = false
    },
  },
})
</script>
