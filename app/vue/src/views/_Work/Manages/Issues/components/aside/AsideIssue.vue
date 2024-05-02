<script lang="ts" setup>
import { inject, type PropType } from 'vue'

defineProps({
  watchers: { type: Array as PropType<{ pk: number; username: string }[]>, default: () => [] },
})

const workManager = inject('workManager')

const delWatcher = (pk: number) => alert(pk)
</script>

<template>
  <!--  <CRow class="mb-3">-->
  <!--    <CCol><h6 class="asideTitle">검색양식</h6></CCol>-->
  <!--  </CRow>-->
  <!--  <CRow class="mb-2">-->
  <!--    <CCol class="col-xxl-5"></CCol>-->
  <!--  </CRow>-->

  <template v-if="workManager && $route.name === '(업무) - 보기'">
    <CRow class="mb-1">
      <CCol>
        <h6 class="asideTitle">업무 관람자 ({{ watchers.length }})</h6>
      </CCol>
      <CCol class="text-right">
        <router-link to="">추가</router-link>
      </CCol>
    </CRow>
    <CRow v-for="watcher in watchers" :key="watcher.pk">
      <CCol class="col-xxl-5">
        <router-link :to="{ name: '사용자 - 보기', params: { userId: watcher.pk } }">
          {{ watcher.username }}
        </router-link>
        <span @click="delWatcher(watcher.pk)">
          <v-icon icon="mdi-trash-can-outline" size="sm" color="grey" class="ml-2 pointer" />
        </span>
      </CCol>
    </CRow>
  </template>
</template>

<style lang="scss" scoped>
.asideTitle {
  font-size: 1.1em;
}
</style>
