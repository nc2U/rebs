<script lang="ts" setup>
import Relation from '@/views/projects/SiteOwner/components/Relation.vue'

const props = defineProps({
  owner: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

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
      @multi-submit="multiSubmit"
      @on-delete="onDelete"
    />
  </CTableRow>
</template>
