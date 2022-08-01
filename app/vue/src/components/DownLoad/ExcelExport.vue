<script lang="ts" setup>
const props = defineProps({
  url: { type: String, default: '' },
  disabled: Boolean,
})
</script>

<template>
  <v-btn
    size="small"
    :href="props.url"
    flat
    width="160"
    :disabled="props.disabled"
    class="mx-3"
    style="text-decoration: none"
  >
    <v-icon icon="mdi-microsoft-excel" color="green" class="mr-2" />
    Excel Export
    <v-icon icon="mdi-download" color="grey" class="ml-2" />
  </v-btn>
</template>
