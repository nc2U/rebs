<script lang="ts" setup>
interface FilterOption {
  value: string
  label: string
  color: string
}

const filterOptions: FilterOption[] = [
  { value: '', label: '전체', color: 'primary' },
  { value: '1', label: '처리대기', color: 'warning' },
  { value: '2', label: '처리중', color: 'primary' },
  { value: '3', label: '처리완료', color: 'success' },
  { value: '4', label: '보류', color: 'secondary' },
]

// Props
const props = defineProps<{
  modelValue: string
}>()

// Events
const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

// 필터 변경
const setFilter = (value: string) => {
  emit('update:modelValue', value)
}
</script>

<template>
  <div class="mb-3 d-flex gap-2">
    <v-chip
      v-for="option in filterOptions"
      :key="option.value"
      :color="props.modelValue === option.value ? option.color : 'default'"
      size="small"
      style="cursor: pointer"
      @click="setFilter(option.value)"
    >
      {{ option.label }}
    </v-chip>
  </div>
</template>
