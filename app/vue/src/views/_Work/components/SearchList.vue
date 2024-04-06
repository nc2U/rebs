<script lang="ts" setup>
import { reactive, ref } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import Multiselect from '@vueform/multiselect'

const condVisible = ref(true)
const optVisible = ref(false)

const searchCond = ref([])

const searxchOptions = reactive([
  { value: 'status', label: '상태' },
  { value: 'project', label: '프로젝트' },
  { value: 'parent', label: '상위 프로젝트' },
  { value: 'is_public', label: '공개여부' },
  { value: 'created', label: '등록일자' },
  { value: 'name', label: '이름' },
  { value: 'description', label: '설명' },
])

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
          <CCol class="col-12 col-md-8">
            <CRow>
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck v-model="searchCond.status" label="상태" id="status" />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">is</option>
                  <option value="0">is not</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">사용중</option>
                  <option value="2">닫힘</option>
                </CFormSelect>
              </CCol>
            </CRow>

            <CRow>
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck v-model="searchCond.status" label="프로젝트" id="project" />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">is</option>
                  <option value="0">is not</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">사용중</option>
                  <option value="2">닫힘</option>
                </CFormSelect>
              </CCol>
            </CRow>

            <CRow>
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck v-model="searchCond.status" label="상위 프로젝트" id="parent" />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">any</option>
                  <option value="1">none</option>
                  <option value="1">is</option>
                  <option value="0">is not</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">사용중</option>
                  <option value="2">닫힘</option>
                </CFormSelect>
              </CCol>
            </CRow>

            <CRow>
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck v-model="searchCond.status" label="공개여부" id="is_public" />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">is</option>
                  <option value="0">is not</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">사용중</option>
                  <option value="2">닫힘</option>
                </CFormSelect>
              </CCol>
            </CRow>

            <CRow>
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck v-model="searchCond.status" label="등록일자" id="created" />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">is</option>
                  <option value="2">&gt;=</option>
                  <option value="3">&lt;=</option>
                  <option value="4">between</option>
                  <option value="5">less than days ago</option>
                  <option value="6">more than days ago</option>
                  <option value="7">is the past</option>
                  <option value="8">days ago</option>
                  <option value="9">today</option>
                  <option value="10">yesterday</option>
                  <option value="11">this week</option>
                  <option value="12">last week</option>
                  <option value="13">last 2 weeks</option>
                  <option value="14">this month</option>
                  <option value="15">last month</option>
                  <option value="16">this year</option>
                  <option value="17">none</option>
                  <option value="18">any</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <DatePicker size="sm" />
              </CCol>
            </CRow>

            <CRow>
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck v-model="searchCond.status" label="이름" id="name" />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">contains</option>
                  <option value="2">contains any of</option>
                  <option value="3">doesn't contain</option>
                  <option value="4">starts with</option>
                  <option value="5">ends with</option>
                  <option value="6">none</option>
                  <option value="7">any</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormInput size="sm" />
              </CCol>
            </CRow>

            <CRow>
              <CCol class="col-4 col-lg-3 col-xl-2 pt-1 mb-3">
                <CFormCheck v-model="searchCond.status" label="설명" id="description" />
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormSelect size="sm" data-width="20">
                  <option value="1">contains</option>
                  <option value="2">contains any of</option>
                  <option value="3">doesn't contain</option>
                  <option value="4">starts with</option>
                  <option value="5">ends with</option>
                  <option value="6">none</option>
                  <option value="7">any</option>
                </CFormSelect>
              </CCol>
              <CCol class="col-4 col-lg-3 col-xl-2">
                <CFormInput size="sm" />
              </CCol>
            </CRow>
          </CCol>

          <CCol md="4" class="text-right">
            <CRow>
              <CFormLabel
                for="searchOptions"
                class="col-4 col-lg-2 col-xl-4 col-xxl-6 col-form-label d-block d-md-none d-lg-block"
              >
                검색조건 추가
              </CFormLabel>
              <CCol class="col-8 col-md-12 col-lg-10 col-xl-8 col-xxl-6">
                <Multiselect
                  size="sm"
                  v-model="searchCond"
                  id="searchOptions"
                  :options="searxchOptions"
                  mode="multiple"
                  placeholder="검색조건 추가"
                />
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
              disabled
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
