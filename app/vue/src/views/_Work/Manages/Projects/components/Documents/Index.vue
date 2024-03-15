<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import NoData from '@/views/_Work/components/NoData.vue'

const emit = defineEmits(['aside-visible'])

const docsList = computed(() => [])

onBeforeMount(() => emit('aside-visible', true))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>문서</h5>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link to="" class="ml-1">새 문서</router-link>
      </span>
    </CCol>
  </CRow>

  <NoData v-if="!docsList.length" />

  <CRow v-else>
    <CCol></CCol>
  </CRow>
</template>
