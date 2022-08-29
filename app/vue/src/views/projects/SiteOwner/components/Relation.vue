<script setup lang="ts">
import { computed, onBeforeMount, reactive, ref, watch } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'

const props = defineProps({
  owner: { type: Object, required: true },
  relation: { type: Object, required: true },
  index: { type: Number, default: 0 },
})

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
})

const sitesNum = computed(() => props.owner.relations.length)

const formSubmit = () => alert('ok')

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
    <CButton color="success" size="sm" @click="formSubmit">적용</CButton>
  </CTableDataCell>
</template>
