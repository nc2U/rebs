<script lang="ts" setup>
import { ref, type PropType } from 'vue'
import type { Category } from '@/store/types/document'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({
  categoryList: { type: Array as PropType<Category[]>, default: () => [] },
})

// defineEmits(['patch-d3-hide'])

const refListModal = ref()

// const patchD3Hide = (pk: number, is_hide: boolean) => emit('patch-d3-hide', { pk, is_hide })

const callModal = () => refListModal.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <AlertModal ref="refListModal" size="lg">
    <template #header> 계정 분류 보기</template>
    <template #default>
      <CListGroup v-for="cate in categoryList" :key="cate.pk" :item-key="cate.pk">
        <CListGroupItem> aaa</CListGroupItem>
      </CListGroup>
    </template>
    <template #footer></template>
  </AlertModal>
</template>
