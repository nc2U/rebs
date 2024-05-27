<script lang="ts" setup>
import { computed } from 'vue'
import { colorLight } from '@/utils/cssMixins'
import NoData from '@/views/_Work/components/NoData.vue'

const versionList = computed(() => [])
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="mr-2 form-text">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '(로드맵) - 추가', query: { back: 1 } }" class="ml-1">
          새 버전
        </router-link>
      </span>
    </CCol>
  </CRow>

  <CRow class="mt-3">
    <CCol>
      <h6>
        <v-icon icon="mdi-check" color="success" size="sm" />
        검색조건
      </h6>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CCard class="mb-3" :color="colorLight">
        <CCardBody>
          <CRow>
            <CFormLabel for="inputEmail3" class="col-sm-1 col-form-label text-right">
              상태
            </CFormLabel>
            <CCol sm="2">
              <CFormSelect>
                <option value="0">모두</option>
                <option value="1">진행</option>
                <option value="2">잠김</option>
                <option value="3">닫힘</option>
              </CFormSelect>
            </CCol>

            <CFormLabel for="inputEmail3" class="col-sm-1 col-form-label text-right">
              버전
            </CFormLabel>
            <CCol sm="2">
              <CFormInput />
            </CCol>

            <CCol class="pt-1">
              <CButton color="primary" size="sm" variant="outline">적용</CButton>
              <span class="ml-2">
                <v-icon icon="mdi-reload" size="sm" color="success" />
                <router-link to="">지우기</router-link>
              </span>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>

  <NoData v-if="!versionList.length" />

  <CRow v-else>
    <CCol></CCol>
  </CRow>
</template>
