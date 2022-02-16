<template>
  <CTable responsive>
    <CTableBody v-if="unitTable.length === 0">
      <CTableRow>
        <CTableDataCell class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>

    <CTableBody v-else>
      <CTableRow class="text-center">
        <Unit class="mt-5" />
        {{ unitTable }}
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Unit from '@/views/projects/Unit/components/Unit.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'UnitListTable',
  components: { Unit },
  computed: {
    ...mapGetters('project', ['unitTable']),
  },
})
</script>
