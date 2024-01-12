<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { write_project } from '@/utils/pageAuth'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({ disabled: Boolean })

const emit = defineEmits(['on-submit'])

const refAlertModal = ref()
const refConfirmModal = ref()

const validated = ref(false)
const form = reactive({
  pay_sort: '',
  pay_code: null as string | null,
  pay_time: null as string | null,
  pay_ratio: null,
  is_pm_cost: false,
  pay_name: '',
  alias_name: '',
  days_since_prev: null as number | null,
  pay_due_date: null as string | null,
  extra_due_date: null as string | null,
})

const onSubmit = (event: Event) => {
  if (write_project.value) {
    const el = event.currentTarget as HTMLSelectElement
    if (!el.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else {
      refConfirmModal.value.callModal()
    }
  } else {
    refAlertModal.value.callModal()
    resetForm()
  }
}

const modalAction = () => {
  emit('on-submit', form)
  validated.value = false
  refConfirmModal.value.close()
  resetForm()
}

const resetForm = () => {
  form.pay_sort = ''
  form.pay_code = null
  form.pay_time = null
  form.pay_ratio = null
  form.is_pm_cost = false
  form.pay_name = ''
  form.alias_name = ''
  form.days_since_prev = null
  form.pay_due_date = null
  form.extra_due_date = null
}
</script>

<template>
  <CForm novalidate class="needs-validation" :validated="validated" @submit.prevent="onSubmit">
    <CTable borderless>
      <colgroup>
        <col style="width: 9%" />
        <col style="width: 9%" />
        <col style="width: 9%" />
        <col style="width: 9%" />
        <col style="width: 9%" />
        <col style="width: 9%" />
        <col style="width: 9%" />
        <col style="width: 9%" />
        <col style="width: 9%" />
        <col style="width: 9%" />
        <col style="width: 10%" />
      </colgroup>
      <CTableBody>
        <CTableRow>
          <CTableDataCell>
            <CFormSelect v-model="form.pay_sort" :disabled="disabled" required>
              <option value="">종류선택</option>
              <option value="1">계약금</option>
              <option value="2">중도금</option>
              <option value="3">잔 금</option>
            </CFormSelect>
          </CTableDataCell>
          <CTableDataCell>
            <CFormInput
              v-model.number="form.pay_code"
              placeholder="납입회차 코드"
              type="number"
              min="0"
              required
              :disabled="disabled"
            />
            <!--        <CFormText>-->
            <!--          프로젝트 내에서 모든 납부회차를 고유 순서대로 숫자로 부여한다.'-->
            <!--        </CFormText>-->
          </CTableDataCell>
          <CTableDataCell>
            <CFormInput
              v-model.number="form.pay_time"
              placeholder="납부순서"
              type="number"
              min="0"
              required
              :disabled="disabled"
            />
            <!--        <CFormText-->
            <!--          >동일 납부회차에 2가지 항목을 별도로 납부하여야 하는 경우(ex: 분담금 +-->
            <!--          업무대행료) 하나의 납입회차 코드(ex: 1)에 2개의 납부순서(ex: 1, 2)를-->
            <!--          등록한다.-->
            <!--        </CFormText>-->
          </CTableDataCell>
          <CTableDataCell>
            <CFormInput
              v-model="form.pay_ratio"
              maxlength="20"
              type="number"
              placeholder="납부비율(공급가대비)"
              :disabled="disabled || form.pay_sort === '3'"
            />
          </CTableDataCell>
          <CTableDataCell>
            <CRow>
              <CFormLabel class="col-md-8 col-form-label"> PM용역비 여부</CFormLabel>
              <CCol md="1" class="pt-2">
                <CFormSwitch v-model="form.is_pm_cost" :disabled="disabled" />
              </CCol>
            </CRow>
          </CTableDataCell>
          <CTableDataCell>
            <CFormInput
              v-model="form.pay_name"
              maxlength="20"
              placeholder="납부회차 명"
              required
              :disabled="disabled"
            />
          </CTableDataCell>
          <CTableDataCell>
            <CFormInput
              v-model="form.alias_name"
              maxlength="20"
              placeholder="별칭 이름"
              :disabled="disabled"
            />
          </CTableDataCell>
          <CTableDataCell>
            <CFormInput
              v-model.number="form.days_since_prev"
              type="number"
              maxlength="20"
              placeholder="전회 기준 경과일수"
              :disabled="disabled"
            />
          </CTableDataCell>
          <CTableDataCell>
            <DatePicker
              v-model="form.pay_due_date"
              maxlength="10"
              placeholder="납부기한일"
              :required="false"
              :disabled="disabled"
            />
          </CTableDataCell>
          <CTableDataCell>
            <DatePicker
              v-model="form.extra_due_date"
              maxlength="10"
              placeholder="납부유예일"
              :required="false"
              :disabled="disabled"
            />
            <!--            <CFormText class="text-grey">-->
            <!--              연체료 계산 기준은 납부기한일이 원칙이나 이 값이 있는 경우-->
            <!--              납부유예일을 연체료 계산 기준으로 한다.-->
            <!--            </CFormText>-->
          </CTableDataCell>
          <CTableDataCell class="text-center">
            <CButton color="primary" type="submit" :disabled="disabled"> 회차추가</CButton>
          </CTableDataCell>
        </CTableRow>
      </CTableBody>
    </CTable>
  </CForm>

  <ConfirmModal ref="refConfirmModal">
    <template #header> 납부 회차 등록</template>
    <template #default> 프로젝트의 납부 회차 정보 등록을 진행하시겠습니까?</template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="refAlertModal" />
</template>
