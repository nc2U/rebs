<script lang="ts" setup>
import { ref } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'

const refIssueForm = ref()
const callModal = () => refIssueForm.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <FormModal ref="refIssueForm"></FormModal>
</template>
