<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useDocument } from '@/store/pinia/document'

const props = defineProps({ tabValue: { type: Number, default: 0 } })

const tab = ref(0)

const documentStore = useDocument()
const categoryList = computed(() => documentStore.categoryList)

watch(props, val => (tab.value = val.tabValue))
</script>

<template>
  <v-card-text>
    <v-window v-model="tab">
      <v-window-item value="all"> 전체</v-window-item>
      <v-window-item
        v-for="cate in categoryList"
        :key="cate.pk"
        :value="cate.pk"
      >
        {{ cate.name }}
      </v-window-item>
    </v-window>
  </v-card-text>
</template>
