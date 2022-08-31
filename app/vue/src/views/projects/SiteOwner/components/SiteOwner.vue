<script lang="ts" setup>
import Relation from '@/views/projects/SiteOwner/components/Relation.vue'

const props = defineProps({
  owner: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['relation-update', 'multi-submit', 'on-delete'])

const relationUpdate = (payload: any) => emit('relation-update', payload)
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (payload: any) => emit('on-delete', payload)
</script>

<template>
  <CTableRow
    v-for="(rel, i) in owner.relations"
    :key="rel.pk"
    class="text-center"
  >
    <Relation
      :owner="owner"
      :relation="rel"
      :index="i"
      @relation-update="relationUpdate"
      @multi-submit="multiSubmit"
      @on-delete="onDelete"
    />
  </CTableRow>
</template>
