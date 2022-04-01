<template>
  <CAlert :color="contractor.status < '3' ? 'success' : 'danger'">
    계약자명 : {{ contractor.name }}({{ contractor.contract.serial_number }})
    :::::: 현재상태 : [{{ getStatus(contractor.status) }}]
  </CAlert>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContractorAlert',
  components: {},
  props: { contractor: Object },
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {},
  methods: {
    getStatus(num: string) {
      const status = [
        { code: '1', text: '청약' },
        { code: '2', text: '계약' },
        { code: '3', text: '청약해지' },
        { code: '4', text: '계약해지' },
      ]
      return status.filter(s => s.code === num).map(s => s.text)[0]
    },
  },
})
</script>
