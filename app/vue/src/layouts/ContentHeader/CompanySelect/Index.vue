<template>
  <CRow>
    <CFormLabel class="col-lg-1 col-form-label text-body">회사명</CFormLabel>
    <CCol md="6" lg="3">
      <CFormSelect @change="$emit('com-select', $event)">
        <option value="">회사선택</option>
        <option
          v-for="com in comSelect"
          :key="com.value"
          :value="com.value"
          :selected="com.value === comId"
        >
          {{ com.text }}
        </option>
      </CFormSelect>
    </CCol>
  </CRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapActions, mapGetters } from 'vuex'

export default defineComponent({
  name: 'CompanySelect',
  props: {
    company: {
      type: Object,
    },
  },
  created() {
    this.fetchCompanyList()
  },
  computed: {
    comId() {
      return this.company ? this.company.pk : this.initComId
    },
    ...mapGetters('settings', ['comSelect']),
    ...mapGetters('accounts', ['initComId']),
  },

  methods: {
    ...mapActions('settings', ['fetchCompanyList']),
  },
})
</script>
