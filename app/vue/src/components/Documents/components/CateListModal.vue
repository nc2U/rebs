<script lang="ts" setup>
import { ref, type PropType } from 'vue'
import type { Category } from '@/store/types/document'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({
  categoryList: { type: Array as PropType<Category[]>, default: () => [] },
})

const emit = defineEmits(['change-cate'])

const refListModal = ref()

const onSubmit = () => {
  emit('change-cate')
}

const callModal = () => refListModal.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <AlertModal ref="refListModal" size="lg">
    <template #header> 카테고리 변경</template>
    <template #default>
      <CListGroup v-for="obj in categoryList" :key="obj.pk" :item-key="obj.pk">
        <CListGroupItem> aaa</CListGroupItem>
      </CListGroup>
    </template>
    <template #footer>
      <CButton color="danger" @click="onSubmit"> 카테고리 변경</CButton>
      <CButton color="light" @click="refListModal.close()">닫기</CButton>
    </template>
  </AlertModal>
</template>
