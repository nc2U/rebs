<script lang="ts" setup>
import { ref, reactive, inject } from 'vue'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const d1List = inject('d1List')
const d2List = inject('d2List')
const orderGroups = inject('orderGroups')
const unitTypes = inject('unitTypes')

defineProps({ disabled: Boolean })
const emit = defineEmits(['on-submit'])

const alertModal = ref()
const confirmModal = ref()

const validated = ref(false)
const form = reactive({
  account_d1: null,
  account_d2: null,
  order_group: null,
  unit_type: null,
  item_name: '',
  average_price: null,
  quantity: null,
  budget: null,
})

const onSubmit = (event: Event) => {
  if (write_project.value) {
    const e = event.currentTarget as HTMLFormElement
    if (!e.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else confirmModal.value.callModal()
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}

const modalAction = () => {
  emit('on-submit', form)
  validated.value = false
  confirmModal.value.visible = false
  resetForm()
}

const resetForm = () => {
  form.account_d1 = null
  form.account_d2 = null
  form.order_group = null
  form.unit_type = null
  form.item_name = ''
  form.average_price = null
  form.quantity = null
  form.budget = null
}
</script>

<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2" color="success">
      <CCol lg="12" xl="5">
        <CRow>
          <CCol md="3" lg="3" class="mb-2">
            <CFormSelect v-model="form.account_d1" required>
              <option value="">대분류</option>
              <option v-for="d1 in d1List" :key="d1.pk" :value="d1.pk">
                {{ d1.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="3" lg="3" class="mb-2">
            <CFormSelect v-model="form.account_d2" required>
              <option value="">중분류</option>
              <option v-for="d2 in d2List" :key="d2.pk" :value="d2.pk">
                {{ d2.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="3" lg="3" class="mb-2">
            <CFormSelect v-model="form.order_group">
              <option value="">차수</option>
              <option
                v-for="og in orderGroups"
                :key="og.value"
                :value="og.value"
              >
                {{ og.label }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="3" lg="3" class="mb-2">
            <CFormSelect v-model="form.unit_type">
              <option value="">타입</option>
              <option v-for="ut in unitTypes" :key="ut.value" :value="ut.value">
                {{ ut.label }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="12" xl="5">
        <CRow>
          <CCol md="3" lg="3" class="mb-2">
            <CFormInput
              v-model="form.item_name"
              placeholder="항목명"
              maxlength="20"
              :disabled="disabled"
            />
          </CCol>

          <CCol md="3" lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.average_price"
              min="0"
              placeholder="평균 가격"
              type="number"
              maxlength="18"
              :disabled="disabled"
            />
          </CCol>
          <CCol md="3" lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.quantity"
              min="0"
              placeholder="수량"
              type="number"
              maxlength="9"
              required
              :disabled="disabled"
            />
          </CCol>
          <CCol md="3" lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.budget"
              min="0"
              placeholder="수입 예산"
              type="number"
              maxlength="18"
              required
              :disabled="disabled"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="12" xl="2" class="d-grid gap-2 d-md-block mb-3">
        <CButton color="primary" type="submit" :disabled="disabled">
          수입 예산 추가
        </CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header> 수입 예산 등록</template>
    <template #default>
      프로젝트의 수입 예산 정보 등록을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
