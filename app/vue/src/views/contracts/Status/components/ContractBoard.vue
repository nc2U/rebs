<template>
  <CContainer>
    <CRow v-if="simpleUnits.length === 0">
      <CCol class="text-center p-5 text-danger">
        등록된 데이터가 없습니다.
      </CCol>
    </CRow>

    <CRow v-else>
      <Building
        v-for="bldg in getBldg"
        :key="bldg"
        :bldg="bldg"
        :maxFloor="maxFloor"
        :units="getUnits(bldg)"
      />
    </CRow>
  </CContainer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Building from '@/views/contracts/Status/components/Building.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ContractBoard',
  components: { Building },
  props: {},
  computed: {
    getBldg(this: any) {
      return [...new Set(this.simpleUnits.map((u: any) => u.bldg))].sort()
    },
    maxFloor(this: any) {
      return Math.max(...this.simpleUnits.map((u: any) => u.floor))
    },
    ...mapGetters('project', ['simpleUnits']),
  },
  methods: {
    getUnits(bldg: number) {
      return this.simpleUnits.filter((u: any) => u.bldg === bldg)
    },
  },
})
</script>
