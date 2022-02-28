<template>
  <CCallout>
    <CRow>
      <CFormLabel class="col-lg-1 col-form-label"> 거래일자</CFormLabel>
      <CCol md="6" lg="3">
        <DatePicker v-model="deal_date" placeholder="거래일자" />
      </CCol>
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import dayjs from 'dayjs'

export default defineComponent({
  name: 'DealDateForm',
  components: { DatePicker },
  data() {
    return {
      deal_date: new Date(),
    }
  },
  computed: {
    date() {
      return this.deal_date ? dayjs(this.deal_date).format('YYYY-MM-DD') : ''
    },
  },
  methods: {},
})
</script>
