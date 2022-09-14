<script setup lang="ts">
import { ref } from 'vue'

const tab = ref('1')
const msg = ref('Category Tabs')
</script>

<template>
  <v-tabs v-model="tab" background-color="" class="mt-5">
    <v-tab value="1">전체</v-tab>
    <v-tab value="2">발송공문</v-tab>
    <v-tab value="3">수신공문</v-tab>
    <v-tab value="4">회의록/보고서</v-tab>
    <v-tab value="5">계약서/협약서</v-tab>
    <v-tab value="6">내규/서식</v-tab>
    <v-tab value="7">기타</v-tab>
  </v-tabs>

  <v-card-text>
    <v-window v-model="tab">
      <v-window-item value="1"> 전체</v-window-item>
      <v-window-item value="2"> 발송공문</v-window-item>
      <v-window-item value="3"> 수신공문</v-window-item>
      <v-window-item value="4"> 회의록/보고서</v-window-item>
      <v-window-item value="5"> 계약서/협약서</v-window-item>
      <v-window-item value="6"> 내규/서식</v-window-item>
      <v-window-item value="7"> 기타</v-window-item>
    </v-window>
  </v-card-text>
</template>
