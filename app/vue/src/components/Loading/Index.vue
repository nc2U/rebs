<script lang="ts" setup>
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/css/index.css'

// loader = 'spinner' | 'dots' | 'bars'
</script>

<template>
  <Loading
    :can-cancel="true"
    :is-full-page="true"
    loader="spinner"
    :height="56"
    :width="56"
    color="#6CBC6F"
    :opacity="0.1"
    background-color="#000"
  />
</template>
