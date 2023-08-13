<script lang="ts" setup>
defineProps({
  modelValue: {
    type: String,
    required: false,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])

const onChange = (event: { target: { files: File[] } }) =>
  emit('update:modelValue', event.target.files[0])
</script>

<template>
  <input type="file" class="form-control" @change="onChange" />
</template>
