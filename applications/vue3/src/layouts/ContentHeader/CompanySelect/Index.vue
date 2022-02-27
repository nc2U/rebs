<template>
  <CRow>
    <CCol md="3">
      <CFormSelect @change="$emit('com-select', $event)">
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
