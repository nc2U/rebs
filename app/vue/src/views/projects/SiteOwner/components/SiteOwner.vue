<script lang="ts" setup>
import { ref } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteOwnerForm from '@/views/projects/SiteOwner/components/SiteOwnerForm.vue'

const props = defineProps({
  owner: {
    type: Object,
    required: true,
  },
  isReturned: { type: Boolean },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (payload: any) => emit('on-delete', payload)
</script>

<template>
  <CTableRow
    v-if="owner"
    class="text-center"
    :style="owner.is_separate ? 'font-weight: bold;' : ''"
  >
    <CTableDataCell>{{ owner.order }}</CTableDataCell>
    <CTableDataCell>
      {{ owner.district }}
    </CTableDataCell>
    <CTableDataCell>
      {{ owner.lot_number }}
    </CTableDataCell>
    <CTableDataCell>
      {{ owner.owner_purpose }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(owner.official_area, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="warning">
      {{ numFormat(owner.official_area, 2) }}
    </CTableDataCell>
    <CTableDataCell v-if="isReturned" class="text-right">
      {{ numFormat(owner.returned_area, 2) }}
    </CTableDataCell>
    <CTableDataCell v-if="isReturned" class="text-right" color="warning">
      {{ numFormat(owner.returned_area, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ owner.owners.join(', ') }}
    </CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      사업 부지 등록
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
