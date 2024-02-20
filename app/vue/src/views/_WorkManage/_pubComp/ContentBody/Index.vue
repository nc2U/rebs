<script lang="ts" setup>
import { ref } from 'vue'

const visible = ref(false)
</script>

<template>
  <CRow class="flex-grow-1">
    <CCol md="10" class="text-body pl-5 p-3 main">
      <slot></slot>
    </CCol>

    <CButton
      color="primary"
      @click="
        () => {
          visible = !visible
        }
      "
      >Toggle offcanvas
    </CButton>

    <COffcanvas
      placement="end"
      :visible="visible"
      @hide="
        () => {
          visible = !visible
        }
      "
    >
      <COffcanvasHeader>
        <COffcanvasTitle>Offcanvas</COffcanvasTitle>
        <CCloseButton
          class="text-reset"
          @click="
            () => {
              visible = false
            }
          "
        />
      </COffcanvasHeader>
      <COffcanvasBody>
        Content for the offcanvas goes here. You can place just about any Bootstrap component or
        custom elements here.
      </COffcanvasBody>
    </COffcanvas>
  </CRow>
</template>

<style lang="scss" scoped>
.main {
  background: #ffffff;
  border-right: 1px solid #ddd !important;
}

.dark-theme .main {
  background: #151620;
  border-right: 1px solid #333 !important;
}
</style>
