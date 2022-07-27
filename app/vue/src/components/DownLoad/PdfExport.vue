<script lang="ts" setup>
import { defineProps } from 'vue'

const props = defineProps({ url: String })
</script>

<template>
  <v-btn size="small" :href="props.url" flat width="180">
    <v-icon icon="mdi-file-pdf-box" color="red" class="mr-2" />
    Pdf Export
    <v-icon icon="mdi-download" color="grey" class="ml-2" />
  </v-btn>
</template>
