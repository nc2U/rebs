<script lang="ts" setup="">
import { reactive } from 'vue'
import { useStore } from 'vuex'
import Multiselect from '@vueform/multiselect'

const isDark = useStore().state.theme === 'dark'
const getUsers = reactive([{ value: 1, label: '고창균' }])
</script>

<template>
  <CCallout color="dark" :class="{ 'bg-light': !isDark }">
    <CRow>
      <CCol md="10" lg="8" xl="6">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label"> 사용자 선택</CFormLabel>
          <CCol>
            <Multiselect
              :options="getUsers"
              placeholder="사용자"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter' | 'tab']"
              searchable
            />
            <!--            v-model.number="form.owner"-->
            <!--            :attrs="form.owner ? {} : { required: true }"-->
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
</template>
