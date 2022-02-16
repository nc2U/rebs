<template>
  <CTable responsive>
    <CTableBody v-if="!sample">
      <CTableRow>
        <CTableDataCell class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>

    <CTableBody v-else>
      <CTableRow class="text-center">
        <Unit class="mt-5" />
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Unit from '@/views/projects/Unit/components/Unit.vue'

export default defineComponent({
  name: 'UnitListTable',
  components: { Unit },
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      sample: true,
    }
  },
  computed: {},
  methods: {},
})
</script>
