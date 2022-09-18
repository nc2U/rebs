<script setup lang="ts">
import { ref, watch } from 'vue'

defineProps({ categoryList: { type: Object, default: null } })
const emit = defineEmits(['select-tab'])

const tab = ref(0)

watch(tab, val => {
  emit('select-tab', val)
})
</script>

<template>
  <v-tabs v-model="tab" background-color="" color="primary" class="mt-5">
    <v-tab :value="0">전체</v-tab>
    <v-tab v-for="cate in categoryList" :key="cate.pk" :value="cate.pk">
      {{ cate.name }}
    </v-tab>
  </v-tabs>
</template>
