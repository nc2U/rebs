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
                v-for="bldg in buildingList"
                :key="bldg.pk"
                :value="bldg.pk"
              >
                {{ bldg.name }}동
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
            <CFormSelect
              v-model="form.type"
              @change="typeSelect"
              :disabled="form.building == ''"
            >
              <option value>---------</option>
              <option
                v-for="type in unitTypeList"
                :value="type.pk"
                :key="type.pk"
              >
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
          <CFormLabel class="col-sm-4 col-form-label"> 시작층</CFormLabel>
          <CCol sm="8">
            <CFormInput
              v-model.number="form.minFloor"
              type="number"
              placeholder="시작층(피로티 제외)"
              :disabled="form.line == ''"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 종료층</CFormLabel>
          <CCol sm="8">
            <CFormInput
              v-model.number="form.maxFloor"
              type="number"
              min="0"
              @keydown.enter="unitRegister"
              placeholder="입력 범위 종료층"
              :disabled="form.minFloor == ''"
            />
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>

  <CAlert color="danger" v-if="warning">
    <CIcon name="cilWarning" />
    <strong> 주의</strong> : 해당 라인에서 시작층부터 종료층까지 범위의
    호수(유니트)가 일괄등록됩니다. 해당 동, 타입과 층을 다시 한번 확인하고
    신중하게 진행하여 주십시요.
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
          [{{ bldgName }}동] ({{ form.type }} 타입) {{ form.line }}호 라인,
          층범위 : {{ form.minFloor }}층 - {{ form.maxFloor }}층
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
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'BuildingSelector',
  components: { ConfirmModal },
  props: {
    project: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      bldgName: '',
      typeName: '',
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
    typeNameLength() {
      const typeNames = this.unitTypeList
        .map((t: any) => t.name)
        .map((t: any) => t.replace(/[^0-9a-zA-Z]/g, ''))
        .map((t: any) => t.length)
      return Math.max.apply({}, typeNames)
    },
    typeMaxUnits() {
      return Math.max.apply(
        {},
        this.unitTypeList.map((t: any) => t.num_unit),
      )
    },
    ...mapState('project', ['unitTypeList', 'buildingList']),
    ...mapGetters('project', ['simpleFloors']),
  },
  watch: {
    project() {
      this.form.building = ''
      this.form.type = ''
    },
    form: {
      deep: true,
      handler(val) {
        if (val.building == '') this.reset(1)
        else if (val.type == '') this.reset(2)
        else if (val.line == '') this.reset(3)
        else if (val.minFloor == '') this.reset(4)
      },
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
      const bldgName = event.target.value
        ? this.buildingList.filter((b: any) => b.pk == event.target.value)[0]
            .name
        : ''
      this.bldgName = bldgName
      const bldg = {
        pk: event.target.value,
        name: bldgName,
      }
      this.$emit('bldg-select', bldg)
    },
    typeSelect(event: any) {
      const typeName = event.target.value
        ? this.unitTypeList.filter((t: any) => t.pk == event.target.value)[0]
            .name
        : ''
      this.typeName = typeName
      this.fetchNumUnitByType({
        project: this.project.pk,
        unit_type: event.target.value,
      })
    },
    unitRegister(this: any) {
      this.$refs.confirmModal.callModal()
    },
    modalAction(this: any) {
      this.$emit('unit-register', {
        ...this.form,
        ...{
          typeName: this.typeName,
          maxLength: this.typeNameLength,
          maxUnits: this.typeMaxUnits,
        },
        ...{ floors: this.simpleFloors },
      })
      this.$refs.confirmModal.visible = false
    },
    ...mapActions('project', ['fetchNumUnitByType']),
  },
})
</script>
