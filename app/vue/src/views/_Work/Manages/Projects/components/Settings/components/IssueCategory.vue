<script lang="ts" setup>
import { type PropType } from 'vue'
import type { SimpleCategory } from '@/store/types/work'
import NoData from '@/views/_Work/components/NoData.vue'

defineProps({ categories: { type: Array as PropType<SimpleCategory[]>, default: () => [] } })
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="mr-2 form-text">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '(설정) - 범주추가' }" class="ml-1">새 업무범주</router-link>
      </span>
    </CCol>
  </CRow>

  <NoData v-if="!categories.length" />

  <CRow v-else>
    <CCol>
      <v-divider class="mb-0" />
      <CTable small striped responsive hover>
        <colgroup>
          <col style="width: 60%" />
          <col style="width: 30%" />
          <col style="width: 10%" />
        </colgroup>
        <CTableHead>
          <CTableRow class="text-center">
            <CTableHeaderCell>업무 범주</CTableHeaderCell>
            <CTableHeaderCell>담당자</CTableHeaderCell>
            <CTableHeaderCell></CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="category in categories" :key="category.pk" class="text-center">
            <CTableDataCell class="text-left">{{ category.name }}</CTableDataCell>
            <CTableDataCell>{{ category.assigned_to?.username }}</CTableDataCell>
            <CTableDataCell class="form-text">
              <span class="mr-2">
                <v-icon icon="mdi-pencil" color="amber" size="sm" class="mr-1" />
                <router-link :to="{ name: '(설정) - 범주수정', params: { cateId: category.pk } }">
                  편집
                </router-link>
              </span>
              <span>
                <v-icon icon="mdi-trash-can" color="grey" size="sm" class="mr-1" />
                <router-link to="">삭제</router-link>
              </span>
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
  </CRow>
</template>
