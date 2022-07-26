<template>
  <CRow>
    <CCol lg="6">
      <CTable hover responsive bordered align="middle">
        <colgroup>
          <col width="25%" />
          <col width="25%" />
          <col width="25%" />
          <col width="25%" />
        </colgroup>
        <CTableBody>
          <CTableRow>
            <CTableHeaderCell color="secondary">총세대수</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.totalNum) }}
            </CTableDataCell>
            <CTableHeaderCell color="secondary">홀딩세대</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.holdNum) }}
            </CTableDataCell>
          </CTableRow>

          <CTableRow>
            <CTableHeaderCell color="success">청약세대</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.appNum) }}
            </CTableDataCell>
            <CTableHeaderCell color="primary">계약세대</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.contNum) }}
            </CTableDataCell>
          </CTableRow>

          <CTableRow>
            <CTableHeaderCell color="secondary">합계</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.appNum + unitSummary.contNum) }}
            </CTableDataCell>
            <CTableHeaderCell color="secondary">잔여세대</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{
                numFormat(
                  unitSummary.totalNum -
                    unitSummary.appNum -
                    unitSummary.contNum,
                )
              }}
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
    <CCol lg="6">
      <span v-for="type in simpleTypes" :key="type.pk" class="mr-3">
        <div class="cube mr-1" :style="`background-color: ${type.color};`" />
        {{ type.name }}
      </span>
    </CCol>
  </CRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ContSummary',
  computed: {
    ...mapState('project', ['houseUnitNum']),
    ...mapGetters('project', ['simpleTypes', 'unitSummary']),
  },
})
</script>

<style lang="scss" scoped>
.cube {
  width: 12px;
  height: 12px;
  display: inline-block;
}
</style>
