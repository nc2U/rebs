<script lang="ts" setup>
const props = defineProps({
  url: { type: String, default: '' },
  disabled: Boolean,
})
</script>

<template>
  <v-row class="justify-end">
    <v-btn
      size="small"
      :href="props.url"
      flat
      width="160"
      :disabled="props.disabled"
      class="mr-3"
    >
      <v-icon icon="mdi-microsoft-excel" color="green" class="mr-2" />
      Excel Export
      <v-icon icon="mdi-download" color="grey" class="ml-2" />
    </v-btn>
  </v-row>
</template>
