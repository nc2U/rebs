<template>
  <CTable hover responsive>
    <colgroup>
      <col width="23%" />
      <col width="23%" />
      <col width="23%" />
      <col width="23%" />
      <col width="8%" />
    </colgroup>
    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell>시작 층</CTableHeaderCell>
        <CTableHeaderCell>종료 층</CTableHeaderCell>
        <CTableHeaderCell>방향/위치(옵션)</CTableHeaderCell>
        <CTableHeaderCell>층별 범위 명칭</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="floorTypeList.length > 0">
      <Floor
        v-for="floor in floorTypeList"
        @on-update="onUpdateFloor"
        @on-delete="onDeleteFloor"
        :key="floor.pk"
        :floor="floor"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell colspan="5" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Floor from '@/views/projects/Floor/components/Floor.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'FloorFormList',
  components: { Floor },
  props: ['project'],
  computed: {
    ...mapState('project', ['floorTypeList']),
  },
  methods: {
    onUpdateFloor(payload: any) {
      this.$emit('on-update', payload)
    },
    onDeleteFloor(pk: number) {
      this.$emit('on-delete', pk)
    },
  },
})
</script>
