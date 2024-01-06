<script setup lang="ts">
import { ref, computed, type PropType } from 'vue'
import { cutString, timeFormat } from '@/utils/baseMixins'
import type { Post } from '@/store/types/document'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  trashPost: { type: Object as PropType<Post>, default: null },
})

const emit = defineEmits(['restore-post'])

const refConfirmModal = ref()

const viewRoute = computed(() => {
  if (props.trashPost?.board === 1) return '공지 사항'
  if (!!props.trashPost?.project) {
    if (props.trashPost.board === 2) return '현장 일반 문서'
    else if (props.trashPost.board === 3) return '현장 소송 문서'
  } else {
    if (props.trashPost?.board === 2) return '본사 일반 문서'
    else if (props.trashPost?.board === 3) return '본사 소송 문서'
  }
  return '공지 사항'
})

const modalAction = () => emit('restore-post', props.trashPost.pk)
</script>

<template>
  <!--  {{ trashPost }}-->
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
    <CTableDataCell>{{ timeFormat(trashPost.deleted) }}</CTableDataCell>
    <CTableDataCell>
      <v-btn density="compact" icon="mdi-delete-restore" size="sm" rounded="1" color="success" />
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="refConfirmModal">
    <template #header> 게시물 정보 복원</template>
    <template #default> 현재 게시물을 휴지통에서 복원 하시겠습니까?</template>
    <template #footer>
      <CButton color="info" @click="modalAction"> 복원</CButton>
    </template>
  </ConfirmModal>
</template>
