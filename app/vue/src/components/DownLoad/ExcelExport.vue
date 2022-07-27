<script lang="ts" setup>
import { defineProps } from 'vue'

const props = defineProps({ url: String })
</script>

<template>
  <v-btn size="small" :href="props.url" flat width="180">
    <v-icon icon="mdi-microsoft-excel" color="green" class="mr-2" />
    Excel Export
    <v-icon icon="mdi-download" color="grey" class="ml-2" />
  </v-btn>
</template>
