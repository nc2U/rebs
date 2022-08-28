<script lang="ts" setup>
import { ref, computed } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteForm from './SiteForm.vue'

const props = defineProps({
  site: {
    type: Object,
    required: true,
  },
  isReturned: { type: Boolean },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const printArray = (arr: string[], sep = ',') => {
  return arr.forEach((el, i) => {
    ;`${el}`
    if (i !== arr.length) `${sep} `
  })
}

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (payload: any) => emit('on-delete', payload)
</script>

<template>
  <CTableRow
    v-if="site"
    class="text-center"
    :style="site.is_separate ? 'font-weight: bold;' : ''"
  >
    <CTableDataCell>{{ site.order }}</CTableDataCell>
    <CTableDataCell>
      {{ site.district }}
    </CTableDataCell>
    <CTableDataCell>
      {{ site.lot_number }}
    </CTableDataCell>
    <CTableDataCell>
      {{ site.site_purpose }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(site.official_area, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(site.official_area, 2) }}
    </CTableDataCell>
    <CTableDataCell v-if="isReturned" class="text-right">
      {{ numFormat(site.returned_area, 2) }}
    </CTableDataCell>
    <CTableDataCell v-if="isReturned" class="text-right">
      {{ numFormat(site.returned_area, 2) }}
    </CTableDataCell>
    <CTableDataCell>
      {{ printArray(site.owners, ',') }}
    </CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      프로젝트 입출금 거래 건별 관리
    </template>
    <template #default>
      <SiteForm
        :site="site"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
