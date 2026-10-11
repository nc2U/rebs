<script lang="ts" setup>
import BankScrapingDialog from '@/components/BankScraping/BankScrapingDialog.vue'

const props = defineProps<{
  modelValue: boolean
  projectId?: number | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'confirmed'): void
}>()
</script>

<template>
  <BankScrapingDialog
    :model-value="props.modelValue"
    mode="project"
    :project-id="props.projectId"
    @update:model-value="emit('update:modelValue', $event)"
    @confirmed="emit('confirmed')"
  />
</template>
