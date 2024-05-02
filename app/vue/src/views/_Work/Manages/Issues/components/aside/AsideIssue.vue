<script lang="ts" setup>
defineProps({ watchers: { type: Array, default: () => [] } })
</script>

<template>
  <!--  <CRow class="mb-3">-->
  <!--    <CCol><h6 class="asideTitle">검색양식</h6></CCol>-->
  <!--  </CRow>-->
  <!--  <CRow class="mb-2">-->
  <!--    <CCol class="col-xxl-5"></CCol>-->
  <!--  </CRow>-->

  <CRow v-if="$route.name === '(업무) - 보기'" class="mb-3">
    <CCol><h6 class="asideTitle">업무 관람자</h6></CCol>
  </CRow>
  <CRow class="mb-2">
    <CCol class="col-xxl-5">
      {{ watchers }}
    </CCol>
  </CRow>
</template>

<style lang="scss" scoped>
.asideTitle {
  font-size: 1.1em;
}
</style>
