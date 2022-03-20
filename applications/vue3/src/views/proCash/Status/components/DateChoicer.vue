<template>
  <CCallout color="success">
    <CRow>
      <CCol md="6" lg="3">
        <DatePicker v-model="date" />
      </CCol>
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from "@/components/DatePicker/index.vue";

export default defineComponent({
  name: 'DateChoicer',
  components: { DatePicker },
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      date: new Date(),
    }
  },
  computed: {},
  methods: {},
})
</script>
