<template>
  <CCard class="mb-4 text-body mx-2 mx-md-3 mx-xl-5">
    <slot name="header">
      <CCardHeader>
        <v-icon icon="mdi mdi-subtitles-outline" size="small" />
        <strong class="pl-1"> {{ $route?.meta.title ?? $route?.name }}</strong>
      </CCardHeader>
    </slot>

    <slot>
      <CCardBody class="pb-5" style="height: 473px"> This page is under construction.</CCardBody>
    </slot>

    <slot name="footer">
      <CCardFooter>&nbsp;</CCardFooter>
    </slot>
  </CCard>
</template>
<script setup lang="ts"></script>
