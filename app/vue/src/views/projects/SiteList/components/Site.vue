<script lang="ts" setup>
import { ref, computed } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteForm from './SiteForm.vue'

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
    <CTableDataCell class="text-left">
      {{ site.lot_number }}
    </CTableDataCell>
    <CTableDataCell>
      {{ site.site_purpose }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ site.official_area }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ site.official_area }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ site.returned_area }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ site.returned_area }}
    </CTableDataCell>
    <CTableDataCell>{{ site.evidence_desc }}</CTableDataCell>
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
