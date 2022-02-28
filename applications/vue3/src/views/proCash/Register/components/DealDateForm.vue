<template>
  <CCallout>
    <CRow>
      <CFormLabel class="col-lg-1 col-form-label">거래일자</CFormLabel>
      <CCol md="6" lg="3">
        <CFormInput
          :value="getToday"
          v-maska="'####-##-##'"
          placeholder="거래일자"
        />
      </CCol>
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { maska } from 'maska'
import moment from 'moment'

export default defineComponent({
  name: 'DealDateForm',
  directives: { maska },
  components: {},
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {
    getToday() {
      const today = new Date()
      return moment(today).format('YYYY-MM-DD')
    },
  },
  methods: {},
})
</script>
