<script lang="ts" setup>
import { defineProps } from 'vue'

const props = defineProps({ url: String })
const downLoad = () => (location.href = `${props.url}`)
</script>

<template>
  <v-btn flat size="small" @click="downLoad">
    <v-icon icon="mdi-microsoft-excel" color="green" class="mr-2" />
    Excel Export
    <v-icon icon="mdi-download" color="grey" class="ml-2" />
  </v-btn>
</template>
