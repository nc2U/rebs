<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect>
        <option value="">---------</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect>
        <option value="">---------</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect>
        <option value="">---------</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput placeholder="적요" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput placeholder="거래처" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect>
        <option value="">---------</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput type="number" placeholder="입금액" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput type="number" placeholder="출금액" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect>
        <option value="">---------</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput placeholder="비고" />
    </CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: '',
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {},
  methods: {},
})
</script>
