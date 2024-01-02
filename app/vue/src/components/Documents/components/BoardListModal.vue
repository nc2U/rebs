<script lang="ts" setup>
import { ref, type PropType } from 'vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import type { Board } from '@/store/types/document'

defineProps({
  boardList: { type: Array as PropType<Board[]>, default: () => [] },
  isCopy: { type: Boolean, default: false },
})

// defineEmits(['patch-d3-hide'])

const refListModal = ref()

// const patchD3Hide = (pk: number, is_hide: boolean) => emit('patch-d3-hide', { pk, is_hide })

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
    <template #footer> </template>
  </AlertModal>
</template>
