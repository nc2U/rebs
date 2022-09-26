<script setup lang="ts">
import { ref, watch, onBeforeMount } from 'vue'

const props = defineProps({
  category: { type: Number, default: 0 },
  categoryList: { type: Object, default: null },
})
const emit = defineEmits(['select-cate'])

const tab = ref(0)

watch(tab, val => {
  emit('select-cate', val)
})

onBeforeMount(() => {
  if (props.category) tab.value = props.category
})
</script>

<template>
  <v-tabs v-model="tab" background-color="" color="success" class="mt-5">
    <v-tab :value="0">전체</v-tab>
    <v-tab v-for="cate in categoryList" :key="cate.pk" :value="cate.pk">
      {{ cate.name }}
    </v-tab>
  </v-tabs>
</template>
