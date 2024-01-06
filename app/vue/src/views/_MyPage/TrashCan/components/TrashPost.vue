<script setup lang="ts">
import { type PropType } from 'vue'
import { cutString, timeFormat } from '@/utils/baseMixins'
import type { TrashPost } from '@/store/types/document'

const props = defineProps({
  trashPost: { type: Object as PropType<TrashPost>, default: null },
  viewRoute: { type: String, default: '' },
})

const emit = defineEmits(['restore-post'])

const restorePost = () => emit('restore-post', props.trashPost.pk)
</script>

<template>
  <CTableRow class="text-center" color="danger">
    <CTableDataCell>{{ trashPost.pk }}</CTableDataCell>
    <CTableDataCell>
      {{ trashPost.board_name }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <span>
        <router-link :to="{ name: `${viewRoute} - 보기`, params: { postId: trashPost.pk } }">
          {{ cutString(trashPost.title || trashPost.title, 50) }}
        </router-link>
      </span>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(trashPost?.deleted) }}</CTableDataCell>
    <CTableDataCell>
      <v-btn
        density="compact"
        icon="mdi-delete-restore"
        size="sm"
        rounded="1"
        color="success"
        @click="restorePost"
      />
    </CTableDataCell>
  </CTableRow>
</template>
