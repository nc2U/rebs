<script lang="ts" setup>
import { ref, type PropType } from 'vue'
import type { Category } from '@/store/types/document'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({
  nowCate: { type: Number, default: null },
  categoryList: { type: Array as PropType<Category[]>, default: () => [] },
})

const emit = defineEmits(['change-cate'])

const refListModal = ref()

const category = ref<number | null>(null)

const selectCate = (cate: number) => (category.value = cate)

const onSubmit = () => {
  emit('change-cate', category.value)
  refListModal.value.close()
}

const callModal = () => refListModal.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <AlertModal ref="refListModal" size="lg">
    <template #header> 카테고리 변경</template>
    <template #default>
      <CTable v-if="categoryList.length" striped class="mt-3 border-top-1">
        <colgroup>
          <col style="width: 90%" />
          <col style="width: 10%" />
        </colgroup>
        <CTableBody>
          <CTableRow v-for="obj in categoryList" :key="obj.pk" :item-key="obj.pk">
            <CTableDataCell>
              <CFormCheck
                type="radio"
                name="board"
                :id="`board_${obj.pk}`"
                :label="obj.name"
                :value="obj.pk"
                :disabled="nowCate === obj.pk"
                @change="selectCate(obj.pk as number)"
              />
            </CTableDataCell>
            <CTableDataCell>
              <CBadge v-if="nowCate === obj.pk" color="warning">현재</CBadge>
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>

      <CRow v-else class="text-center">
        <CCol class="py-5">해당 게시판에 카테고리가 없습니다.</CCol>
      </CRow>
    </template>
    <template #footer>
      <CButton color="danger" @click="onSubmit" :disabled="!category"> 카테고리 변경</CButton>
      <CButton color="light" @click="refListModal.close()">닫기</CButton>
    </template>
  </AlertModal>
</template>
