<script lang="ts" setup>
import { computed } from 'vue'
import type { Contractor, ContractRelease } from '@/store/types/contract'
import { AlertLight } from '@/utils/cssMixins'

const props = defineProps<{
  contractor?: Contractor | null
  contRelease?: ContractRelease | null
}>()

const emit = defineEmits<{
  'call-form': [contractorId: number]
}>()

const isSuccession = computed(
  () => !!props.contractor?.succession && props.contractor?.succession.status !== '3',
)

const callFormModal = () => {
  if (props.contractor?.pk) {
    emit('call-form', props.contractor.pk)
  }
}
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="text-end">
    <v-btn
      :color="contRelease ? 'brown-lighten-2' : 'warning'"
      :disabled="isSuccession"
      @click="callFormModal"
    >
      {{ contRelease ? '수정하기' : '등록하기' }}
    </v-btn>
  </CAlert>
</template>
