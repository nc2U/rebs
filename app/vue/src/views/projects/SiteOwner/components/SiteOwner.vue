<script lang="ts" setup>
import { computed, ref } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import Relation from '@/views/projects/SiteOwner/components/Relation.vue'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteOwnerForm from '@/views/projects/SiteOwner/components/SiteOwnerForm.vue'

const props = defineProps({
  owner: {
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
    v-for="(rel, i) in owner.relations"
    :key="rel.pk"
    class="text-center"
  >
    <Relation :owner="owner" :relation="rel" :index="i" />
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
