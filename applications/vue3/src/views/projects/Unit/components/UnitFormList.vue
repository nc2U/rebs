<template>
  <CTable hover responsive>
    <colgroup>
      <col width="50%" />
      <col width="50%" />
    </colgroup>
    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell>동(건물)이름</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="unitList.length > 0">
      <Unit
        v-for="unit in unitList"
        @on-update="onUpdateUnit"
        @on-delete="onDeleteUnit"
        :key="unit.pk"
        :unit="unit"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell colspan="2" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Unit from '@/views/projects/Unit/components/Unit.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'UnitFormList',
  components: { Unit },
  props: ['project'],
  computed: {
    ...mapState('project', ['unitList']),
  },
  methods: {
    onUpdateUnit(payload: any) {
      this.$emit('on-update', payload)
    },
    onDeleteUnit(pk: number) {
      this.$emit('on-delete', pk)
    },
  },
})
</script>
