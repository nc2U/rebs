<script setup lang="ts">
import ContentBody from '@/layouts/ContentBody/Index.vue'
</script>

<template>
  <ContentBody>
    <CCardBody class="blank-body text-center">
      <span> Authorization not granted! </span>
      <p class="text-medium-emphasis">
        이 페이지에 대한 열람 권한이 없습니다. 관리자에게 문의하여 주십시요.
      </p>
    </CCardBody>
  </ContentBody>
</template>

<style lang="scss" scoped>
.card-body {
  height: 600px;
  padding-top: 230px;
}

.card-body span {
  color: darkred;
  font-size: 2em;
  line-height: 80px;
}
</style>
