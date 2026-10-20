<script lang="ts" setup>
import { computed, inject, reactive, ref } from 'vue'
import { usePerms } from '@/composables/usePerms'
import type { UnitType } from '@/store/types/project'
import AlertModal from '@/components/Modals/AlertModal.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

defineProps({ disabled: Boolean })
const emit = defineEmits<{
  (e: 'on-submit', payload: Omit<UnitType, 'pk' | 'project'>): void
}>()

const { can, PERM } = usePerms()
const canProjectUpdate = computed(() => can(PERM.PROJECT_UPDATE))

export type SortType = {
  value: '1' | '2' | '3' | '4' | '5' | '6'
  label: string
}

const typeSort = inject<SortType[]>('typeSort')

const refAlertModal = ref()
const refConfirmModal = ref()

const validated = ref(false)
const form = reactive<{
  sort: '1' | '2' | '3' | '4' | '5' | '6' | ''
  main_or_sub: '1' | '2' | ''
  name: string
  color: string
  actual_area: number | '' | null
  supply_area: number | '' | null
  contract_area: number | '' | null
  average_price: number | '' | null
  price_setting: '1' | '2' | '3' | ''
  num_unit: number | '' | null
}>({
  sort: '',
  main_or_sub: '1',
  name: '',
  color: '#000000',
  actual_area: null,
  supply_area: null,
  contract_area: null,
  average_price: null,
  price_setting: '',
  num_unit: null,
})

const onSubmit = (event: Event) => {
  if (canProjectUpdate.value) {
    const el = event.currentTarget as HTMLFormElement
    if (!el.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else {
      refConfirmModal.value?.callModal()
    }
  } else {
    refAlertModal.value?.callModal()
    resetForm()
  }
}

const modalAction = () => {
  emit('on-submit', {
    sort: form.sort,
    main_or_sub: form.main_or_sub,
    name: form.name.trim(),
    color: form.color,
    actual_area:
      form.actual_area !== null && form.actual_area !== '' ? Number(form.actual_area) : null,
    supply_area:
      form.supply_area !== null && form.supply_area !== '' ? Number(form.supply_area) : null,
    contract_area:
      form.contract_area !== null && form.contract_area !== '' ? Number(form.contract_area) : null,
    average_price:
      form.average_price !== null && form.average_price !== '' ? Number(form.average_price) : null,
    price_setting: form.price_setting,
    num_unit: form.num_unit !== null && form.num_unit !== '' ? Number(form.num_unit) : null,
  })
  validated.value = false
  refConfirmModal.value?.close()
  resetForm()
}

const resetForm = () => {
  form.sort = ''
  form.main_or_sub = '1'
  form.name = ''
  form.color = '#000000'
  form.actual_area = null
  form.supply_area = null
  form.contract_area = null
  form.average_price = null
  form.price_setting = ''
  form.num_unit = null
}
</script>

<template>
  <CForm novalidate class="needs-validation" :validated="validated" @submit.prevent="onSubmit">
    <CRow class="p-2">
      <CCol lg="3">
        <CRow>
          <CCol lg="4" class="mb-2">
            <CFormSelect v-model="form.sort" required :disabled="disabled">
              <option value="">타입종류</option>
              <option v-for="tp in typeSort" :key="tp.value" :value="tp.value">
                {{ tp.label }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol lg="4" class="mb-2">
            <CFormSelect v-model="form.main_or_sub" required :disabled="disabled">
              <option value="1">메인유닛</option>
              <option value="2">보조시설</option>
            </CFormSelect>
          </CCol>

          <CCol lg="4" class="mb-2">
            <CFormInput
              v-model="form.name"
              maxlength="10"
              placeholder="타입명칭"
              required
              :disabled="disabled"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="1">
        <CRow>
          <CCol lg="12" class="mb-2">
            <CFormInput
              v-model="form.color"
              title="타입색상"
              type="color"
              required
              :disabled="disabled"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="7">
        <CRow>
          <CCol lg="2" class="mb-2">
            <CFormInput
              v-model.number="form.actual_area"
              placeholder="전용면적"
              type="number"
              min="0"
              step="0.0001"
              :disabled="disabled"
            />
            <CFormFeedback invalid>전용면적을 소수점 4자리 이하로 입력하세요.</CFormFeedback>
          </CCol>
          <CCol lg="2" class="mb-2">
            <CFormInput
              v-model.number="form.supply_area"
              placeholder="공급면적"
              type="number"
              min="0"
              step="0.0001"
              :disabled="disabled"
            />
            <CFormFeedback invalid>공급면적을 소수점 4자리 이하로 입력하세요.</CFormFeedback>
          </CCol>
          <CCol lg="2" class="mb-2">
            <CFormInput
              v-model.number="form.contract_area"
              placeholder="계약면적"
              type="number"
              min="0"
              step="0.0001"
              :disabled="disabled"
            />
            <CFormFeedback invalid>계약면적을 소수점 4자리 이하로 입력하세요.</CFormFeedback>
          </CCol>

          <CCol lg="2" class="mb-2">
            <CFormInput
              v-model.number="form.average_price"
              placeholder="평균가격"
              type="number"
              min="0"
              :disabled="disabled"
            />
          </CCol>

          <CCol lg="2" class="mb-2">
            <CFormSelect v-model="form.price_setting" required :disabled="disabled">
              <option value="">공급가 설정 옵션</option>
              <option value="1">타입별 설정</option>
              <option value="2">층타입별 설정</option>
              <option value="3">호별 설정</option>
            </CFormSelect>
          </CCol>

          <CCol lg="2" class="mb-2">
            <CFormInput
              v-model.number="form.num_unit"
              placeholder="세대수"
              type="number"
              min="0"
              required
              :disabled="disabled"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="1">
        <CRow>
          <CCol lg="12" class="d-grid gap-2 d-lg-block mb-3">
            <v-btn color="primary" type="submit" :disabled="disabled">타입추가</v-btn>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="refConfirmModal">
    <template #header>타입 정보 등록</template>
    <template #default>프로젝트의 타입 정보 등록을 진행하시겠습니까?</template>
    <template #footer>
      <v-btn color="primary" size="small" @click="modalAction">저장</v-btn>
    </template>
  </ConfirmModal>

  <AlertModal ref="refAlertModal" />
</template>
