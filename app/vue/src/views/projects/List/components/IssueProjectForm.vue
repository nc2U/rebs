<script lang="ts" setup>
import { ref } from 'vue'
import ProjectForm from '@/views/_Work/Manages/Projects/components/ProjectForm.vue'
import FormModal from '@/components/Modals/FormModal.vue'

const refIssueForm = ref()
const callModal = () => refIssueForm.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <FormModal ref="refIssueForm" :size="'xl'">
    <template #header>새 업무 프로젝트 생성</template>
    <template #default>
      <CModalBody class="text-body">
        <ProjectForm />
      </CModalBody>
    </template>
  </FormModal>
</template>
