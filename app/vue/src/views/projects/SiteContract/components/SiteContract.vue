<script lang="ts" setup>
import { ref } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteContractForm from './SiteContractForm.vue'

const props = defineProps({
  site: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

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
    <CTableDataCell class="text-right" color="warning">
      {{ numFormat(site.official_area, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(site.returned_area, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="warning">
      {{ numFormat(site.returned_area, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-left"> </CTableDataCell>
    <CTableDataCell></CTableDataCell>
    <CTableDataCell></CTableDataCell>
    <CTableDataCell></CTableDataCell>
    <CTableDataCell></CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      부지 매입 계약 등록
    </template>
    <template #default>
      <SiteContractForm
        :site="site"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
