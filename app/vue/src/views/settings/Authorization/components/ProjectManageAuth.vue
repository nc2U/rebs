<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import Multiselect from '@vueform/multiselect'

const isDark = useStore().state.theme === 'dark'
const getProjects = reactive([
  { value: 1, label: '송도센트럴자이' },
  { value: 2, label: '아야진프로젝트' },
])
const isInActive = ref(false)
</script>

<template>
  <CCallout color="secondary" class="mb-4" :class="{ 'bg-light': !isDark }">
    <CRow>
      <CCol md="10" lg="8" xl="6">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label">
            허용 프로젝트
          </CFormLabel>
          <CCol>
            <Multiselect
              :options="getProjects"
              placeholder="프로젝트"
              mode="tags"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
              :disabled="isInActive"
            />
            <!--            v-model.number="form.owner"-->
            <!--            :attrs="form.owner ? {} : { required: true }"-->
            <small class="form-text">
              사용자가 조회 및 관리할 수 있는 프로젝트들을 선택합니다.
            </small>
          </CCol>
        </CRow>
      </CCol>

      <CCol md="10" lg="8" xl="6">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label">
            담당 메인 프로젝트
          </CFormLabel>
          <CCol>
            <Multiselect
              :options="getProjects"
              placeholder="프로젝트"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
              :disabled="isInActive"
            />
            <!--            v-model.number="form.owner"-->
            <!--            :attrs="form.owner ? {} : { required: true }"-->
            <small class="form-text">
              사용자의 각 화면에서 선택한 프로젝트를 기본 프로젝트로 보여줍니다.
            </small>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
  <hr />
</template>
