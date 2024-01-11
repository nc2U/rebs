<script lang="ts" setup>
import { computed, type PropType } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { type Contractor } from '@/store/types/contract'
import { AlertLight } from '@/utils/cssMixins'

const props = defineProps({
  contractor: { type: Object as PropType<Contractor>, default: null },
})
const emit = defineEmits(['call-form'])

const contractStore = useContract()
const contRelease = computed(() => contractStore.contRelease)

const isSuccession = computed(
  () => !!props.contractor?.succession && !props.contractor?.succession.is_approval,
)

const callFormModal = () => emit('call-form', props.contractor.pk)
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="text-right">
    <CButton
      :color="contRelease ? 'warning' : 'danger'"
      :disabled="isSuccession"
      @click="callFormModal"
    >
      {{ contRelease ? '수정하기' : '등록하기' }}
    </CButton>
  </CAlert>
</template>
