<script lang="ts" setup>
import { ref, reactive, computed, watch, onBeforeMount, onUpdated } from 'vue'
import { useAccount } from '@/store/pinia/account'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { write_project } from '@/utils/pageAuth'

const props = defineProps({
  floor: { type: Object, default: null },
  condTexts: { type: Object, default: null },
  queryIds: { type: Object, default: null },
  price: { type: Object, default: null },
})

const emit = defineEmits(['on-create', 'on-update', 'on-delete'])

const alertModal = ref()
const confirmModal = ref()

const form = reactive({
  price_build: null as number | null,
  price_land: null as number | null,
  price_tax: null as number | null,
  price: null as number | null,
})

watch(form, val => {
  if (!val.price_build) form.price_build = null
  if (!val.price_land) form.price_land = null
  if (!val.price_tax) form.price_tax = null
  if (!val.price) form.price = null
})

watch(props, val => {
  if (val.price) initForm()
})

onBeforeMount(() => initForm())
onUpdated(() => {
  resetForm()
  initForm()
})

const btnColor = computed(() => (props.price ? 'success' : 'primary'))
const btnTitle = computed(() => (props.price ? '수정' : '등록'))

const formsCheck = computed(() => {
  if (props.price) {
    const a = form.price_build === props.price.price_build
    const b = form.price_land === props.price.price_land
    const c = form.price_tax === props.price.price_tax
    const d = form.price === props.price.price || !props.price
    return a && b && c && d
  } else {
    return (
      !form.price_build && !form.price_land && !form.price_tax && !form.price
    )
  }
})

const onStorePrice = () => {
  if (write_project.value) {
    const payload = {
      ...props.queryIds,
      ...{ unit_floor_type: props.floor.pk },
      ...form,
    }
    if (!props.price) emit('on-create', payload)
    else {
      const updatePayload = { ...{ pk: props.price.pk }, ...payload }
      emit('on-update', updatePayload)
    }
  } else alertModal.value.callModal()
}

const deletePrice = () => {
  if (useAccount().superAuth) confirmModal.value.callModal()
  else alertModal.value.callModal()
}
const modalAction = () => {
  emit('on-delete', props.price.pk)
  confirmModal.value.close()
  resetForm()
}

const initForm = () => {
  if (props.price) {
    form.price_build = props.price.price_build
    form.price_land = props.price.price_land
    form.price_tax = props.price.price_tax
    form.price = props.price.price
  }
}

const resetForm = () => {
  form.price_build = null
  form.price_land = null
  form.price_tax = null
  form.price = null
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
        @keydown.enter="onStorePrice"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_land"
        type="number"
        min="0"
        placeholder="타입별 대지가"
        @keydown.enter="onStorePrice"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_tax"
        type="number"
        min="0"
        placeholder="타입별 부가세"
        @keydown.enter="onStorePrice"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price"
        type="number"
        min="0"
        placeholder="타입별 공급가격"
        @keydown.enter="onStorePrice"
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
      <CButton color="danger" size="sm" :disabled="!price" @click="deletePrice">
        삭제
      </CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header> 공급가격 삭제 </template>
    <template #default>
      삭제 후 복구할 수 없습니다. 해당 공급가격 정보를 삭제 하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
