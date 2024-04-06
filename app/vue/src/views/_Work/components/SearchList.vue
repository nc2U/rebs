<script lang="ts" setup>
import { ref } from 'vue'

const condVisible = ref(true)
const optVisible = ref(false)

const searchCond = ref({
  status: true,
})

const viewMode = ref<'board' | 'list'>('board')
</script>

<template>
  <CRow>
    <CCol class="pointer pt-1 mb-0" @click="condVisible = !condVisible">
      <v-icon :icon="condVisible ? 'mdi-chevron-down' : 'mdi-chevron-right'" size="sm" />
      검색조건
    </CCol>
    <v-divider class="mx-3 mt-2 mb-0" />

    <CCollapse :visible="condVisible">
      <slot name="condition">
        <CRow class="m-2" color="light">
          <CCol class="col-4 col-md-3 col-lg-2 pt-1 mb-3">
            <CFormCheck v-model="searchCond.status" label="상태" id="status" />
          </CCol>
          <CCol class="col-4 col-md-3 col-lg-2">
            <CFormSelect size="sm" data-width="20">
              <option value="1">사용중</option>
              <option value="2">닫힘</option>
            </CFormSelect>
          </CCol>
          <CCol class="col-4 col-md-3 col-lg-2">
            <CFormSelect size="sm" data-width="20">
              <option value="1">사용중</option>
              <option value="2">닫힘</option>
            </CFormSelect>
          </CCol>
          <CCol class="col-md-3 col-lg-6 text-right">
            <CRow>
              <CCol class="d-none d-lg-block"></CCol>
              <CCol class="col-lg-4">
                <CFormSelect size="sm">
                  <option value="">검색조건 추가</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </slot>
    </CCollapse>
  </CRow>

  <CRow class="mt-2">
    <CCol class="pointer mb-0" @click="optVisible = !optVisible">
      <v-icon :icon="optVisible ? 'mdi-chevron-down' : 'mdi-chevron-right'" size="sm" />
      옵션
    </CCol>
    <v-divider class="mx-3 mt-2 mb-0" />
    <CCollapse :visible="optVisible">
      <slot name="option">
        <CRow class="m-2" color="light">
          <CCol>
            <span class="mr-3">결과 표시 </span>
            <CFormCheck
              v-model="viewMode"
              label="보드"
              name="viewMode"
              value="board"
              inline
              type="radio"
            />
            <CFormCheck
              v-model="viewMode"
              label="목록"
              name="viewMode"
              value="list"
              inline
              type="radio"
            />
          </CCol>
        </CRow>
      </slot>
    </CCollapse>
  </CRow>

  <CRow class="my-3">
    <CCol>
      <slot name="footer">
        <router-link to="" class="mr-3">
          <v-icon icon="mdi-check-bold" size="sm" color="success" />
          검색
        </router-link>
        <router-link to="" class="mr-3">
          <v-icon icon="mdi-replay" size="sm" color="success" />
          초기화
        </router-link>
        <!--        <router-link to=""> Save 검색양식</router-link>-->
      </slot>
    </CCol>
  </CRow>
</template>
