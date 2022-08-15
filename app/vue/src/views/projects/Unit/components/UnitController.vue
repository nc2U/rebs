<script lang="ts" setup>
import { computed, reactive, ref, watch } from 'vue'
import { useStore } from 'vuex'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import project from '@/store/modules/project'
import { write_project } from '@/utils/pageAuth'

const props = defineProps({
  project: {
    type: Number,
    required: true,
  },
})

const bldgName = ref('')
const typeName = ref('')
const form = reactive({
  building: '',
  line: '',
  type: '',
  minFloor: '',
  maxFloor: '',
})

watch(props, () => {
  form.building = ''
})

const warning = computed(() => form.maxFloor !== '')
const typeNameLength = computed(() => {
  const typeNames = unitTypeList.value
    .map((t: any) => t.name)
    .map((t: any) => t.replace(/[^0-9a-zA-Z]/g, ''))
    .map((t: any) => t.length)
  return Math.max.apply({}, typeNames)
})

const typeMaxUnits = computed(() =>
  Math.max.apply(
    {},
    unitTypeList.value.map((t: any) => t.num_unit),
  ),
)

const store = useStore()
const unitTypeList = computed(() => store.state.project.unitTypeList)
const buildingList = computed(() => store.state.project.buildingList)
const simpleFloors = computed(() => store.getters['project/simpleFloors'])

const fetchNumUnitByType = (payload: any) =>
  store.dispatch('project/fetchNumUnitByType', payload)

watch(project, () => {
  form.building = ''
  form.type = ''
})

watch(form, val => {
  if (val.building == '') reset(1)
  else if (val.line == '') reset(2)
  else if (val.type == '') reset(3)
  else if (val.minFloor == '') reset(4)
})

const reset = (n: number) => {
  if (n == 1) {
    form.line = ''
    form.type = ''
    form.minFloor = ''
    form.maxFloor = ''
  } else if (n == 2) {
    form.type = ''
    form.minFloor = ''
    form.maxFloor = ''
  } else if (n == 3) {
    form.minFloor = ''
    form.maxFloor = ''
  } else {
    form.maxFloor = ''
  }
}
const emit = defineEmits(['bldg-select', 'unit-register'])
const confirmModal = ref()
const alertModal = ref()

const bldgSelect = (event: any) => {
  const bdName = event.target.value
    ? buildingList.value.filter((b: any) => b.pk == event.target.value)[0].name
    : ''
  bldgName.value = bdName
  const bldg = {
    pk: event.target.value,
    name: bdName,
  }
  emit('bldg-select', bldg)
}
const typeSelect = (event: any) => {
  const tpName = event.target.value
    ? unitTypeList.value.filter((t: any) => t.pk == event.target.value)[0].name
    : ''
  typeName.value = tpName
  fetchNumUnitByType({
    project: props.project,
    unit_type: event.target.value,
  })
}
const unitRegister = () => {
  if (write_project) confirmModal.value.callModal()
  else {
    alertModal.value.callModal()
    reset(1)
  }
}
const modalAction = () => {
  emit('unit-register', {
    ...form,
    ...{
      typeName: typeName.value,
      maxLength: typeNameLength.value,
      maxUnits: typeMaxUnits.value,
    },
    ...{ floors: simpleFloors.value },
  })
  confirmModal.value.visible = false
  reset(1)
}
</script>

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
              :disabled="!project"
              @change="bldgSelect"
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
          <CFormLabel class="col-sm-4 col-form-label"> 등록라인</CFormLabel>
          <CCol sm="8">
            <CFormInput
              v-model.number="form.line"
              type="number"
              min="0"
              placeholder="등록할 라인 숫자 입력"
              :disabled="form.building == ''"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol md="3" class="mb-2">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label"> 타입선택</CFormLabel>
          <CCol sm="8">
            <CFormSelect
              v-model="form.type"
              :disabled="form.line == ''"
              @change="typeSelect"
            >
              <option value>---------</option>
              <option
                v-for="type in unitTypeList"
                :key="type.pk"
                :value="type.pk"
              >
                {{ type.name }}
              </option>
            </CFormSelect>
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
              :disabled="form.type == ''"
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
              placeholder="입력 범위 종료층"
              :disabled="form.minFloor == ''"
              @keydown.enter="unitRegister"
            />
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>

  <CAlert v-if="warning" color="danger">
    <CIcon name="cilWarning" />
    <strong> 주의</strong> : 해당 라인에서 시작층부터 종료층까지 범위의
    호수(유니트)가 일괄등록됩니다. 해당 동, 타입과 층을 다시 한번 확인하고
    신중하게 진행하여 주십시요.
  </CAlert>

  <CAlert color="secondary" class="text-right">
    <CButton
      color="primary"
      :disabled="form.minFloor === ''"
      @click="unitRegister"
    >
      호수(유니트) 일괄등록
    </CButton>
  </CAlert>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cilItalic" />
      호수(유니트) 정보
    </template>
    <template #default>
      <p class="text-primary">
        <strong>
          [{{ bldgName }}동] ({{ form.type }} 타입) {{ form.line }}호 라인,
          층범위 : {{ form.minFloor }}층 - {{ form.maxFloor }}층
        </strong>
      </p>
      <p>상기 호수(유니트)정보의 일괄등록을 진행하시겠습니까?</p>
    </template>
    <template #footer>
      <CButton color="primary" @click="modalAction">일괄등록</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
