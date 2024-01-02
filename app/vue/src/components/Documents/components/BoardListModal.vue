<script lang="ts" setup>
import { ref, type PropType } from 'vue'
import type { Board } from '@/store/types/document'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  boardList: { type: Array as PropType<Board[]>, default: () => [] },
  isCopy: { type: Boolean, default: false },
})

const emit = defineEmits(['copy-post', 'move-post'])

const refListModal = ref()

const onSubmit = () => {
  if (props.isCopy) emit('copy-post')
  else emit('move-post')
}

const callModal = () => refListModal.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <AlertModal ref="refListModal" size="lg">
    <template #header> 게시판 {{ isCopy ? '복사' : '이동' }}</template>
    <template #default>
      <CListGroup v-for="obj in boardList" :key="obj.pk" :item-key="obj.pk">
        <CListGroupItem> aaa</CListGroupItem>
      </CListGroup>
    </template>
    <template #footer>
      <CButton color="danger" @click="onSubmit">게시물 {{ isCopy ? '복사' : '이동' }}</CButton>
      <CButton color="light" @click="refListModal.close()">닫기</CButton>
    </template>
  </AlertModal>
</template>
