<script lang="ts" setup>
import { useStore } from '@/store'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const store = useStore()
</script>

<template>
  <MdEditor
    language="en-US"
    codeTheme="atom"
    :toolbarsExclude="['github']"
    style="height: 250px"
    :theme="store.theme"
  />
</template>

<style lang="scss" scoped>
.dark-theme .md-editor {
  background: #2f303b !important;
}

.md-editor-dark {
  --md-bk-color: #474850;
}
</style>
