<script lang="ts" setup>
import { ref, type PropType } from 'vue'
import type { Board } from '@/store/types/document'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  nowBoard: { type: Number, default: null },
  boardList: { type: Array as PropType<Board[]>, default: () => [] },
  isCopy: { type: Boolean, default: false },
})

const emit = defineEmits(['copy-post', 'move-post'])

const refListModal = ref()

const board = ref<number | null>(null)

const selectBoard = (brd: number) => (board.value = brd)

const onSubmit = () => {
  if (props.isCopy) emit('copy-post', board.value)
  else emit('move-post', board.value)
  refListModal.value.close()
}

const callModal = () => refListModal.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <AlertModal ref="refListModal" size="lg">
    <template #header> 게시판 {{ isCopy ? '복사' : '이동' }}</template>
    <template #default>
      <CTable striped class="mt-3 border-top-1">
        <colgroup>
          <col style="width: 90%" />
          <col style="width: 10%" />
        </colgroup>
        <CTableBody>
          <CTableRow v-for="obj in boardList" :key="obj.pk" :item-key="obj.pk">
            <CTableDataCell>
              <CFormCheck
                type="radio"
                name="board"
                :id="`board_${obj.pk}`"
                :label="obj.name"
                :value="obj.pk"
                :disabled="nowBoard === obj.pk"
                @change="selectBoard(obj.pk as number)"
              />
            </CTableDataCell>
            <CTableDataCell>
              <CBadge v-if="nowBoard === obj.pk" color="warning">현재</CBadge>
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </template>
    <template #footer>
      <CButton :color="isCopy ? 'warning' : 'danger'" @click="onSubmit">
        게시물 {{ isCopy ? '복사' : '이동' }}
      </CButton>
      <CButton color="light" @click="refListModal.close()">닫기</CButton>
    </template>
  </AlertModal>
</template>
