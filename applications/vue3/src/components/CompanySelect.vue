<template>
  <CRow>
    <CCol md="4">
      <CFormSelect @change="$emit('on-change', $event)">
        <option value="">회사선택</option>
        <option
          v-for="com in comSelect"
          :value="com.value"
          :selected="com.value === comId"
          :key="com.value"
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
  created() {
    this.fetchCompanyList()
  },
  props: {
    company: {
      type: Object,
    },
  },
  computed: {
    comId() {
      return this.company ? this.company.id : ''
    },
    ...mapGetters('settings', ['comSelect']),
  },

  methods: {
    ...mapActions('settings', ['fetchCompanyList']),
  },
})
</script>
