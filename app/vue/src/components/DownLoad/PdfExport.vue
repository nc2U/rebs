<script lang="ts" setup>
const props = defineProps({
  url: { type: String, default: '' },
  disabled: Boolean,
})
</script>

<template>
  <v-row class="justify-end my-1">
    <v-col class="my-0 py-1">
      <slot />
    </v-col>
    <slot name="near" />
    <v-btn
      size="small"
      :href="props.url"
      flat
      width="160"
      :disabled="props.disabled"
      class="mx-3"
    >
      <v-icon icon="mdi-file-pdf-box" color="red" class="mr-2" />
      Pdf Export
      <v-icon icon="mdi-download" color="grey" class="ml-2" />
    </v-btn>
  </v-row>
</template>
