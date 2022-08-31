<script setup lang="ts">
import { computed, onBeforeMount, reactive, ref, watch } from 'vue'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteOwnerForm from '@/views/projects/SiteOwner/components/SiteOwnerForm.vue'

const props = defineProps({
  owner: { type: Object, required: true },
  relation: { type: Object, required: true },
  index: { type: Number, default: 0 },
})

const emit = defineEmits(['relation-update', 'multi-submit', 'on-delete'])

const updateFormModal = ref()

const form = reactive({
  pk: null,
  site: null,
  ownership_ratio: '',
  owned_area: '',
  acquisition_date: null as null | string,
})

const calcArea = ref(0)

watch(form, val => {
  if (val.owned_area) calcArea.value = parseInt(val.owned_area) * 0.3025
  else calcArea.value = 0

  if (val.acquisition_date)
    form.acquisition_date = dateFormat(val.acquisition_date)
})

const sitesNum = computed(() => props.owner.relations.length)

const relationUpdate = (payload: any) => emit('relation-update', payload)
const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (payload: any) => emit('on-delete', payload)

onBeforeMount(() => {
  if (props.relation) {
    form.pk = props.relation.pk
    form.site = props.relation.site
    form.ownership_ratio = props.relation.ownership_ratio
    form.owned_area = props.relation.owned_area
    form.acquisition_date = props.relation.acquisition_date
    calcArea.value = props.relation.owned_area * 0.3025
  }
})
</script>

<template>
  <CTableDataCell v-if="index === 0" :rowspan="sitesNum">
    {{ owner.own_sort_desc }}
  </CTableDataCell>
  <CTableDataCell v-if="index === 0" :rowspan="sitesNum">
    {{ owner.owner }}
  </CTableDataCell>
  <CTableDataCell v-if="index === 0" :rowspan="sitesNum">
    {{ owner.date_of_birth }}
  </CTableDataCell>
  <CTableDataCell v-if="index === 0" :rowspan="sitesNum">
    {{ owner.phone1 }}
  </CTableDataCell>
  <CTableDataCell>
    {{ relation.site.lot_number }}
  </CTableDataCell>
  <CTableDataCell class="text-right">
    <CFormInput
      v-model.number="form.ownership_ratio"
      type="number"
      min="0"
      step="0.0001"
      placeholder="소유지분(%)"
    />
  </CTableDataCell>
  <CTableDataCell class="text-right">
    <CFormInput
      v-model.number="form.owned_area"
      type="number"
      min="0"
      step="0.0001"
      placeholder="면적(제곱미터)"
    />
  </CTableDataCell>
  <CTableDataCell class="text-right" color="warning">
    {{ numFormat(calcArea, 4) }}
  </CTableDataCell>
  <CTableDataCell class="text-left">
    <DatePicker
      v-model="form.acquisition_date"
      type="number"
      placeholder="소유권 취득일"
    />
  </CTableDataCell>
  <CTableDataCell>
    <CButton color="success" size="sm" @click="relationUpdate(form)">
      적용
    </CButton>
  </CTableDataCell>
  <CTableDataCell v-if="index === 0" :rowspan="sitesNum">
    <CButton color="info" size="sm" @click="showDetail"> 확인</CButton>
  </CTableDataCell>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      부지 소유자 정보 관리
    </template>
    <template #default>
      <SiteOwnerForm
        :owner="owner"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
