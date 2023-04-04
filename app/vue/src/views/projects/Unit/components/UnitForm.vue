<script lang="ts" setup="">
import { computed, onMounted, ref } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { useProjectData } from '@/store/pinia/project_data'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({ unit: { type: Object, required: true } })
const emit = defineEmits(['on-update', 'on-delete'])

const alertModal = ref()
const confirmModal = ref()

const form = ref({
  unit_type: null,
  // floor_type: null,
  name: '',
  // bldg_line: null,
  // floor_no: null,
  is_hold: false,
  hold_reason: '',
})

const formCheck = computed(() => {
  if (props.unit) {
    const a = form.value.unit_type === props.unit.unit_type
    // const b = form.value.floor_type === props.unit.floor_type
    const b = form.value.name === props.unit.name
    // const d = form.value.bldg_line === props.unit.bldg_line
    // const e = form.value.floor_no === props.unit.floor_no
    const c = form.value.is_hold === props.unit.is_hold
    const d = form.value.hold_reason === props.unit.hold_reason

    return a && b && c && d
  } else return false
})

const proDataStore = useProjectData()
const getTypes = computed(() => proDataStore.getTypes)
// const getFloorTypes = computed(() => proDataStore.getFloorTypes)

const onUpdateUnit = () => {
  if (write_project) {
    const pk = props.unit.pk
    emit('on-update', { ...{ pk }, ...form.value })
  } else alertModal.value.callModal()
}

const onDeleteUnit = () => {
  if (useAccount().superAuth) confirmModal.value.callModal()
  else alertModal.value.callModal()
}

const delConfirm = () => {
  emit('on-delete', props.unit.pk)
  confirmModal.value.close()
}

onMounted(() => {
  if (props.unit) {
    form.value.unit_type = props.unit.unit_type
    // form.value.floor_type = props.unit.floor_type
    form.value.name = props.unit.name
    // form.value.bldg_line = props.unit.bldg_line
    // form.value.floor_no = props.unit.floor_no
    form.value.is_hold = props.unit.is_hold
    form.value.hold_reason = props.unit.hold_reason
  }
})
</script>

<template>
  <CTableRow class="text-center">
    <CTableDataCell>
      <CFormSelect v-model="form.unit_type" reqired>
        <option value="">타입</option>
        <option v-for="ut in getTypes" :key="ut.value" :value="ut.value">
          {{ ut.label }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <!--    <CTableDataCell>-->
    <!--      <CFormSelect v-model="form.floor_type" reqired>-->
    <!--        <option value="">층범위타입</option>-->
    <!--        <option v-for="fl in getFloorTypes" :key="fl.value" :value="fl.value">-->
    <!--          {{ fl.label }}-->
    <!--        </option>-->
    <!--      </CFormSelect>-->
    <!--    </CTableDataCell>-->
    <CTableDataCell>
      <CFormInput
        v-model="form.name"
        maxlength="5"
        placeholder="호수"
        reqired
      />
    </CTableDataCell>
    <!--    <CTableDataCell>-->
    <!--      <CFormInput-->
    <!--        v-model.number="form.bldg_line"-->
    <!--        type="number"-->
    <!--        num="0"-->
    <!--        placeholder="라인"-->
    <!--        reqired-->
    <!--      />-->
    <!--    </CTableDataCell>-->
    <!--    <CTableDataCell>-->
    <!--      <CFormInput-->
    <!--        v-model.number="form.floor_no"-->
    <!--        type="number"-->
    <!--        num="0"-->
    <!--        placeholder="층수"-->
    <!--        reqired-->
    <!--      />-->
    <!--    </CTableDataCell>-->
    <CTableDataCell>
      <CFormCheck v-model="form.is_hold" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.hold_reason"
        maxlength="100"
        placeholder="홀딩 사유"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CButton
        color="success"
        size="sm"
        :disabled="formCheck"
        @click="onUpdateUnit"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteUnit">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header> 호수 유닛 삭제</template>
    <template #default>
      이 호수에 종속된 계약 건 데이터가 있는 경우 해당 데이터를 모두 제거한 후
      삭제가능 합니다. 해당 호수 유닛을 삭제 하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="delConfirm">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
