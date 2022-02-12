<template>
  <CTable hover responsive>
    <colgroup>
      <col width="25%" />
      <col width="10%" />
      <col width="25%" />
      <col width="25%" />
      <col width="15%" />
    </colgroup>
    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell>타입명칭</CTableHeaderCell>
        <CTableHeaderCell>타입색상</CTableHeaderCell>
        <CTableHeaderCell>평균가격</CTableHeaderCell>
        <CTableHeaderCell>세대수</CTableHeaderCell>
        <CTableHeaderCell>비 고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="unitTypeList.length > 0">
      <Type
        v-for="type in unitTypeList"
        @on-update="onUpdateType"
        @on-delete="onDeleteType"
        :key="type.pk"
        :type="type"
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
import Type from '@/views/projects/Type/components/Type.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'TypeFormList',
  components: { Type },
  props: ['project'],
  computed: {
    ...mapState('project', ['unitTypeList']),
  },
  methods: {
    onUpdateType(payload: any) {
      this.$emit('on-update', payload)
    },
    onDeleteType(pk: number) {
      this.$emit('on-delete', pk)
    },
  },
})
</script>
