<script lang="ts" setup="">
import {ref} from 'vue'
import Multiselect from '@vueform/multiselect'

const msg = ref('유저 셀렉트')
const getUsers = [{value: 1, label: '고창균'},]
</script>

<template>
  <CCallout color="info">
    <CRow>
      <CCol md="6" lg="4">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label"> 사용자 선택</CFormLabel>
          <CCol>
            <Multiselect
                :options="getUsers"
                placeholder="사용자"
                autocomplete="label"
                :classes="{ search: 'form-control multiselect-search' }"
                :add-option-on="['enter' | 'tab']"
                searchable/>
            <!--            v-model.number="form.owner"-->
            <!--            :attrs="form.owner ? {} : { required: true }"-->
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
</template>
