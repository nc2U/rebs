<script lang="ts" setup>
import { type PropType } from 'vue'
import type { Version } from '@/store/types/work'

defineProps({ version: { type: Object as PropType<Version>, required: true } })

const boxClass = ['primary-box', 'danger-box', 'success-box']
</script>

<template>
  <CCol>
    <CRow class="mb-3">
      <CCol>
        <v-icon icon="mdi-star-box-multiple" color="amber" class="mr-2" />
        <span class="mr-2 bold" style="font-size: large">
          <router-link :to="{ name: '(로드맵) - 보기', params: { verId: version.pk } }">
            {{ version.name }}
          </router-link>
        </span>

        <span :class="boxClass[Number(version.status) - 1]">
          {{ version.status_desc }}
        </span>
      </CCol>
      <CCol v-if="1 == 1" class="text-right">
        <!-- 관리자 권한 있을 때 렌더링 -->
        <v-icon icon="mdi-pencil" color="amber" size="18" />
      </CCol>
    </CRow>

    <CRow>
      <CCol class="col-sm-10 col-md-8 col-lg-6 col-xl-4 p-0 mx-2">
        <CProgress color="success" :value="50" :style="{ '--cui-border-radius': 0 }">
          50%
        </CProgress>
      </CCol>
    </CRow>
    <CRow class="mb-4">
      <CCol class="form-text">
        <span>
          <router-link to="">6 업무</router-link>
        </span>
        <span>( <router-link to="">5 건 완료</router-link> - </span>
        <span> <router-link to="">한 건 진행 중</router-link>) </span>
      </CCol>
    </CRow>

    <CRow>
      <CCol class="mb-4">
        <h6>연결된 업무</h6>
        <v-divider class="mb-0" />
        <CTable responsive hover small striped>
          <colgroup>
            <col style="width: 3%" />
            <col style="width: 94%" />
            <col style="width: 3%" />
          </colgroup>
          <CTableBody>
            <CTableRow v-for="i in 3" :key="i">
              <CTableDataCell>a</CTableDataCell>
              <CTableDataCell>b</CTableDataCell>
              <CTableDataCell class="text-center">c</CTableDataCell>
            </CTableRow>
          </CTableBody>
        </CTable>
      </CCol>
    </CRow>
  </CCol>
</template>
