<script lang="ts" setup>
const emit = defineEmits(['close-form'])
const closeForm = () => emit('close-form')
</script>

<template>
  <div>{{ 'edit form' }}</div>

  <CButton type="button" color="light" @click="closeForm" size="sm">취소</CButton>
</template>
