<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import SearchList from '@/views/_Work/components/SearchList.vue'
import NoData from '@/views/_Work/components/NoData.vue'

const emit = defineEmits(['aside-visible'])

const timeEntryList = computed(() => [])

onBeforeMount(() => emit('aside-visible', true))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>소요시간</h5>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link to="" class="ml-1">작업시간 기록</router-link>
      </span>
    </CCol>
  </CRow>

  <SearchList />

  <NoData v-if="!timeEntryList.length" />

  <CRow v-else>
    <CCol></CCol>
  </CRow>
</template>
