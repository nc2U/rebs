<template>
  <CCallout color="success">
    <CRow>
      <CFormLabel class="col-lg-1 col-form-label">기준일자</CFormLabel>
      <CCol md="6" lg="3">
        <DatePicker v-model="date" @keydown.enter="setDate" />
      </CCol>
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'

export default defineComponent({
  name: 'DateChoicer',
  components: { DatePicker },
  data() {
    return {
      date: new Date(),
    }
  },
  watch: {
    date() {
      this.setDate()
    },
  },
  methods: {
    setDate(this: any) {
      this.$emit('set-date', this.dateFormat(this.date))
    },
  },
})
</script>
