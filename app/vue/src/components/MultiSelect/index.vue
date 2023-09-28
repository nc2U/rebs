<script setup lang="ts">
import Multiselect from '@vueform/multiselect'
</script>

<template>
  <Multiselect
    mode="tags"
    autocomplete="label"
    :classes="{
      caret: 'multiselect-caret mr-4',
      search: 'form-control multiselect-search',
      tagsSearch: 'form-control multiselect-tags-search',
    }"
    :add-option-on="['enter', 'tab']"
    searchable
  />
</template>
