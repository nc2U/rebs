<script lang="ts" setup="">
import { ref } from 'vue'

const msg = ref('DocsForm')
</script>

<template>
  <span v-if="$route.params.postId">
    {{ $route.params.postId }}
  </span>
  <br />
  {{ msg }}
</template>
