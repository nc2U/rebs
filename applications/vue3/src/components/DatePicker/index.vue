<template>
  <Datepicker
    name="date-picker"
    textInput
    autoApply
    :format="dateFormat"
    position="left"
    :textInputOptions="textInputOptions"
    inputClassName="form-control"
    :enableTimePicker="false"
    v-maska="'####-##-##'"
    teleport="#app"
    :dark="dark"
    required
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Datepicker from 'vue3-date-time-picker'
import moment from 'moment'
import { maska } from 'maska'

export default defineComponent({
  name: 'DatePicker',
  directives: { maska },
  components: { Datepicker },
  props: {},
  setup() {
    return {}
  },
  computed: {
    textInputOptions() {
      return {
        enterSubmit: true,
        tabSubmit: true,
        openMenu: true,
        format: 'yyyy-MM-dd',
      }
    },
    dark(this: any) {
      return this.$store.state.theme === 'dark'
    },
  },
  methods: {
    dateFormat: (date: any) => moment(date).format('YYYY-MM-DD'),
  },
})
</script>
