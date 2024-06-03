<script lang="ts" setup>
import type { PropType } from 'vue'
import type { CodeValue } from '@/store/types/work'

defineProps({
  activities: { type: Array as PropType<CodeValue[]>, default: () => [] },
  activityList: { type: Array as PropType<CodeValue[]>, default: () => [] },
})
</script>

<template>
  <CRow class="py-2">
    <CCol class="text-right form-text">
      <span>
        <v-icon icon="mdi-trash-can" color="secondary" size="sm" />
        <router-link to="" class="ml-1">초기화</router-link>
      </span>

      <span class="ml-2">
        <v-icon icon="mdi-cog" color="secondary" size="sm" />
        <router-link :to="{ name: '코드값' }" class="ml-1">관리</router-link>
      </span>
    </CCol>
  </CRow>
  {{ activities }}
  <CRow>
    <CCol>
      <v-divider class="my-0" />
      <CTable hover small striped responsive>
        <colgroup>
          <col style="width: 30%" />
          <col style="width: 30%" />
          <col style="width: 30%" />
        </colgroup>
        <CTableHead>
          <CTableRow class="text-center">
            <CTableHeaderCell scope="col">이름</CTableHeaderCell>
            <CTableHeaderCell scope="col">시스템 작업</CTableHeaderCell>
            <CTableHeaderCell scope="col">
              <v-icon icon="mdi-check" size="sm" color="success" />
              사용중
            </CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="act in activityList" :key="act.pk" class="text-center">
            <CTableDataCell class="text-left pl-2">{{ act.name }}</CTableDataCell>
            <CTableDataCell>
              <v-icon icon="mdi-check" size="sm" color="success" />
            </CTableDataCell>
            <CTableDataCell>
              <CFormCheck />
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CButton color="primary" size="sm" variant="outline">저장</CButton>
    </CCol>
  </CRow>
</template>
