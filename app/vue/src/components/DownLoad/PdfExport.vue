<script lang="ts" setup>
import { defineProps } from 'vue'

const props = defineProps({ url: String })
const downLoad = () => (location.href = `${props.url}`)
</script>

<template>
  <v-btn variant="flat" size="small" @click="downLoad">
    <v-icon icon="mdi-file-pdf-box" color="red" class="mr-2" />
    Pdf Export
    <v-icon icon="mdi-download" color="grey" class="ml-2" />
  </v-btn>
</template>
