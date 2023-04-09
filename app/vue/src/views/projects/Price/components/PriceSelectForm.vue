<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  project: { type: Number, default: null },
  orders: { type: Object, default: null },
  types: { type: Object, default: null },
})

const emit = defineEmits([
  'on-order-select',
  'on-type-select',
  'cont-price-set',
])

const confirmModal = ref()

const order = ref<number | null>(null)
const type = ref<number | null>(null)

watch(props, () => {
  order.value = null
  type.value = null
})

const onOrderSelect = (e: Event) => {
  type.value = null
  emit('on-order-select', (e.target as HTMLSelectElement).value)
}
const onTypeSelect = (e: Event) =>
  emit('on-type-select', (e.target as HTMLSelectElement).value)

const accStore = useAccount()
const superAuth = computed(() => accStore.superAuth)

const contPriceSet = () => confirmModal.value.callModal()

const modalAction = () => {
  emit('cont-price-set')
  confirmModal.value.close()
}
</script>

<template>
  <CCallout color="warning" class="pb-2 mb-4">
    <CRow>
      <CCol md="4" class="mb-2">
        <CRow>
          <CFormLabel for="sel1" class="col-sm-3 col-form-label">
            차수선택
          </CFormLabel>
          <CCol sm="9">
            <CFormSelect id="sel1" v-model="order" @change="onOrderSelect">
              <option value="">---------</option>
              <option v-for="o in orders" :key="o.pk" :value="o.pk">
                {{ o.order_group_name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol md="4" class="mb-2">
        <CRow>
          <CFormLabel for="sel2" class="col-sm-3 col-form-label">
            타입선택
          </CFormLabel>
          <CCol sm="9">
            <CFormSelect
              id="sel2"
              v-model="type"
              :disabled="!order"
              @change="onTypeSelect"
            >
              <option value="">---------</option>
              <option v-for="t in types" :key="t.pk" :value="t.pk">
                {{ t.name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol md="4" class="mb-2">
        <CRow class="justify-content-end">
          <CCol xl="6" class="d-grid gap-2">
            <CButton
              v-if="superAuth"
              type="button"
              color="dark"
              :disabled="!project"
              @click="contPriceSet"
            >
              전체 계약건 공급가 재설정
            </CButton>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>

  <ConfirmModal ref="confirmModal">
    <template #icon>
      <v-icon icon="mdi mdi-sync-alert" color="danger" class="mr-2" />
    </template>
    <template #header> 전체 계약건 공급가 재설정</template>
    <template #default>
      이 작업은 현재 등록된 전체 계약 건의 공급가를 현재 가격 데이터로 일괄
      변경합니다.<br /><br />
      이 작업은 수 분 정도 소요될 수 있습니다.<br />
      전체 계약 건 개별 공급가를 현재 등록된 가격 정보로 재설정하시겠습니까?
    </template>
    <template #footer>
      <CButton color="dark" @click="modalAction">재설정</CButton>
    </template>
  </ConfirmModal>
</template>
