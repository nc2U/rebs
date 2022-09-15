<template>
  <CCard class="mb-4 text-body">
    <slot name="header">
      <CCardHeader>
        <CIcon name="cil-notes" />
        <strong class="pl-1"> {{ $route.meta.title || $route.name }}</strong>
      </CCardHeader>
    </slot>

    <slot>
      <CCardBody class="pb-5"> This page is under construction.</CCardBody>

      <CCardFooter>&nbsp;</CCardFooter>
    </slot>
  </CCard>
</template>
