<script lang="ts" setup>
import { ref, reactive, computed, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { usePayment } from '@/store/pinia/payment'
import { Price } from '@/store/types/payment'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { write_project } from '@/utils/pageAuth'

const props = defineProps({
  floor: { type: Object, default: null },
  condTexts: { type: Object, default: null },
  queryIds: { type: Object, default: null },
})
const emit = defineEmits(['on-create', 'on-update', 'on-delete'])

const alertModal = ref()
const confirmModal = ref()

const price = ref({
  pk: null as number | null,
  price_build: null as number | null,
  price_land: null as number | null,
  price_tax: null as number | null,
  price: null as number | null,
})
const form = reactive({
  price_build: null as number | null,
  price_land: null as number | null,
  price_tax: null as number | null,
  price: null as number | null,
})

watch(form, val => {
  if (!!val.price_build) form.price_build = null
  if (!!val.price_land) form.price_land = null
  if (!!val.price_tax) form.price_tax = null
  if (!!val.price) form.price = null
})

const btnColor = computed(() => (price.value ? 'success' : 'primary'))
const btnTitle = computed(() => (price.value ? '수정' : '등록'))

const formsCheck = computed(() => {
  if (price.value) {
    const a = form.price_build == price.value.price_build
    const b = form.price_land == price.value.price_land
    const c = form.price_tax == price.value.price_tax
    const d = form.price == price.value.price
    return (a && b && c && d) || !price.value
  } else {
    return (
      !form.price_build && !form.price_land && !form.price_tax && !form.price
    )
  }
})

const paymentStore = usePayment()
const priceList = computed(() => paymentStore.priceList)

watch(priceList, () => resetForm())

const onStorePrice = () => {
  if (write_project) {
    const payload = {
      ...props.queryIds,
      ...{ unit_floor_type: props.floor.pk },
      ...form,
    }
    if (!price.value) emit('on-create', payload)
    else {
      const updatePayload = { ...{ pk: price.value.pk }, ...payload }
      emit('on-update', updatePayload)
    }
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}

const deletePrice = () => {
  if (useAccount().superAuth) confirmModal.value.callModal()
  else {
    alertModal.value.callModal()
    resetForm()
  }
}
const modalAction = () => {
  emit('on-delete', price.value.pk)
  confirmModal.value.visible = false
}

const resetForm = () => {
  const unit_floor_type = props.floor.pk
  const { project, order_group, unit_type } = props.queryIds

  price.value = priceList.value.filter(
    (p: Price) =>
      p.project === project &&
      p.order_group === order_group &&
      p.unit_type === unit_type &&
      p.unit_floor_type === unit_floor_type,
  )[0]

  if (price.value) {
    form.price_build = price.value.price_build
    form.price_land = price.value.price_land
    form.price_tax = price.value.price_tax
    form.price = price.value.price
  }
}
</script>

<template>
  <CTableRow>
    <CTableDataCell class="text-center">
      {{ condTexts.orderText }}
    </CTableDataCell>
    <CTableDataCell class="text-center">
      {{ condTexts.typeText }}
    </CTableDataCell>
    <CTableDataCell>
      {{ floor.alias_name }}
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_build"
        type="number"
        min="0"
        placeholder="타입별 건물가"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_land"
        type="number"
        min="0"
        placeholder="타입별 대지가"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_tax"
        type="number"
        min="0"
        placeholder="타입별 부가세"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price"
        type="number"
        min="0"
        placeholder="타입별 공급가격"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        :color="btnColor"
        size="sm"
        :disabled="formsCheck"
        @click="onStorePrice"
      >
        {{ btnTitle }}
      </CButton>
      <CButton
        color="danger"
        size="sm"
        :disabled="!price"
        @click="deletePrice()"
      >
        삭제
      </CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-warning" />
      공급가격 삭제
    </template>
    <template #default>
      이 그룹에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후 삭제가능
      합니다. 해당 공급가격을 삭제 하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
