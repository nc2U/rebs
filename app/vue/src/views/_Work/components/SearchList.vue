<script lang="ts" setup="">
import { ref } from 'vue'

const msg = ref('Search List!')
</script>

<template>
  <div>{{ $route.name }} - {{ msg }}</div>
</template>
