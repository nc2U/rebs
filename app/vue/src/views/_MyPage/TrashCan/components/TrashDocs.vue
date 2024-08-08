<script setup lang="ts">
import { type PropType } from 'vue'
import type { TrashDocs } from '@/store/types/docs'
import { cutString, timeFormat } from '@/utils/baseMixins'

const props = defineProps({
  trashDocs: { type: Object as PropType<TrashDocs>, default: null },
  viewRoute: { type: String, default: '' },
})

const emit = defineEmits(['restore-docs'])

const restoreDocs = () => emit('restore-docs', props.trashDocs.pk)
</script>

<template>
  <CTableRow class="text-center" color="danger">
    <CTableDataCell>{{ trashDocs.pk }}</CTableDataCell>
    <CTableDataCell>
      {{ trashDocs.type_name }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <span>
        <router-link :to="{ name: `${viewRoute} - 보기`, params: { docsId: trashDocs.pk } }">
          {{ cutString(trashDocs.title || trashDocs.title, 50) }}
        </router-link>
      </span>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(trashDocs?.deleted) }}</CTableDataCell>
    <CTableDataCell>
      <v-btn
        density="compact"
        icon="mdi-delete-restore"
        size="sm"
        rounded="1"
        color="success"
        @click="restoreDocs"
      />
    </CTableDataCell>
  </CTableRow>
</template>
