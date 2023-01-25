<script lang="ts" setup>
import {ref} from 'vue'
import Multiselect from '@vueform/multiselect'

const msg = ref('프로젝트 관리')
const getProjects = [{value: 1, label: '송도센트럴자이'}, {value: 2, label: '아야진프로젝트'}]
const isInActive = false
</script>

<template>
  <CCallout color="secondary" class="mb-4">
    <CRow>
      <CCol md="6" lg="4">
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
                :disabled="isInActive"/>
            <!--            v-model.number="form.owner"-->
            <!--            :attrs="form.owner ? {} : { required: true }"-->
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <CRow>
      <CCol md="6" lg="4">
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
                :disabled="isInActive"/>
            <!--            v-model.number="form.owner"-->
            <!--            :attrs="form.owner ? {} : { required: true }"-->
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
  <hr/>
</template>
