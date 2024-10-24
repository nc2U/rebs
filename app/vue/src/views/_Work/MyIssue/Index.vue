<script setup lang="ts">
import { ref, reactive, onBeforeMount } from 'vue'
import { GridLayout, type LayoutItemRequired } from 'grid-layout-plus'
import MultiSelect from '@/components/MultiSelect/index.vue'

const showItems = ref(['1', '2'])

const selectOptions = [
  { value: '1', label: '내가 맡은 업무' },
  { value: '2', label: '보고한 업무' },
  { value: '3', label: '수정한 업무' },
  { value: '4', label: '지켜 보고 있는 업무' },
  { value: '5', label: '업무' },
  { value: '6', label: '최근 뉴스' },
  { value: '7', label: '달력' },
  { value: '8', label: '문서' },
  { value: '9', label: '소요시간' },
  { value: '10', label: '작업내역' },
]

const layouts = reactive([])

const item1 = reactive({ x: 0, y: 0, w: 6, h: 3, i: '내가 맡은 업무 (0)' })
const item2 = reactive({ x: 6, y: 0, w: 6, h: 3, i: '보고한 업무 (0)' })
const item3 = reactive({ x: 0, y: 0, w: 12, h: 3, i: '수정한 업무 (0)' })
const item4 = reactive({ x: 0, y: 0, w: 12, h: 3, i: '지켜 보고 있는 업무 (0)' })
const item5 = reactive({ x: 0, y: 0, w: 12, h: 3, i: '업무 (0)' })
const item6 = reactive({ x: 0, y: 0, w: 12, h: 3, i: '최근 뉴스 (0)' })
const item7 = reactive({ x: 0, y: 0, w: 12, h: 3, i: '달력 (0)' })
const item8 = reactive({ x: 0, y: 0, w: 12, h: 3, i: '문서 (0)' })
const item9 = reactive({ x: 0, y: 0, w: 12, h: 3, i: '소요시간 (0)' })
const item10 = reactive({ x: 0, y: 0, w: 12, h: 3, i: '작업내역 (0)' })

const itemPush = (item: string) => {
  layouts.push(eval(`item${item}`))
  layouts.sort((a, b) => a.localeCompare(b))
}

const itemRemove = (item: string) => {
  let index = layouts.indexOf(eval(`item${item}`))
  if (index > -1) layouts.splice(index, 1)
}

interface LayoutItem extends LayoutItemRequired {
  minW?: number
  minH?: number
  maxW?: number
  maxH?: number
  moved?: boolean
  static?: boolean
  isDraggable?: boolean
  isResizable?: boolean
}

type Layout = Array<LayoutItem>
type Breakpoint = 'xxs' | 'xs' | 'sm' | 'md' | 'lg'
type Breakpoints = Record<Breakpoint, number>
type ResponsiveLayout = Record<Breakpoint, Layout>

onBeforeMount(() => {
  showItems.value.forEach(item => {
    layouts.push(eval(`item${item}`))
  })
})
</script>

<template>
  <CCard>
    <CCardBody>
      <CRow class="px-2">
        <CCol style="display: flex; justify-content: flex-end">
          <MultiSelect
            v-model="showItems"
            :options="selectOptions"
            placeholder="추가하기"
            class="multiselect-blue"
            @select="itemPush($event)"
            @deselect="itemRemove($event)"
          />
        </CCol>
      </CRow>
      <!-- Item slot usage -->
      <GridLayout
        v-model:layout="layouts"
        :col-num="12"
        :row-height="30"
        is-draggable
        is-resizable
        vertical-compact
        use-css-transforms
      >
        <template #item="{ item }">
          <div class="w-100 h-100 border p-3">
            <CRow class="px-2 mb-1">
              <CCol>{{ item.i }}</CCol>
            </CRow>
            <CAlert color="warning">표시할 데이터가 없습니다.</CAlert>
          </div>
        </template>
      </GridLayout>
    </CCardBody>
  </CCard>
</template>

<style lang="scss" scoped>
.multiselect-blue {
  --ms-tag-bg: #dbeafe;
  --ms-tag-color: #2563eb;
}
</style>
