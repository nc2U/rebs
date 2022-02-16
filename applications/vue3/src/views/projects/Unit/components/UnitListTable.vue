<template>
  <CContainer>
    <CRow v-if="unitTable.length === 0">
      <CCol class="text-center p-5 text-danger">
        등록된 데이터가 없습니다.
      </CCol>
    </CRow>

    <CRow v-else>
      <CCol class="p-5" md="5">
        <CTable responsive>
          <CTableBody>
            <CTableRow v-for="i in maxFloor" :key="i">
              <Unit
                v-for="line in lineList"
                :key="line"
                :units="unitTable"
                :floor="maxFloor + 1 - i"
                :line="line"
              />
            </CTableRow>
          </CTableBody>
        </CTable>
      </CCol>
    </CRow>
  </CContainer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Unit from '@/views/projects/Unit/components/Unit.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'UnitListTable',
  components: { Unit },
  computed: {
    maxFloor(this: any) {
      return Math.max(...this.unitTable.map((u: any) => u.floor))
    },
    lineList(this: any) {
      return [...new Set(this.unitTable.map((u: any) => u.line))]
    },
    ...mapGetters('project', ['unitTable']),
  },
})
</script>
