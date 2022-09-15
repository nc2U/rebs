<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useDocument } from '@/store/pinia/document'

const emit = defineEmits(['select-tab'])

const tab = ref(0)
const documentStore = useDocument()
const categoryList = computed(() => documentStore.categoryList)

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
