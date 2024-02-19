<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from '@/store'

const visible = ref(false)
const isDark = computed(() => useStore().theme === 'dark')
const backGround = computed(() => (isDark.value ? 'bg-dark' : 'bg-white'))
</script>

<template>
  <CRow class="flex-grow-1">
    <CCol md="10" class="text-body pl-4 p-3 main" :class="backGround">a</CCol>
    <CCol class="text-body p-3">b</CCol>

    <!--    <CButton-->
    <!--      color="primary"-->
    <!--      @click="-->
    <!--        () => {-->
    <!--          visible = !visible-->
    <!--        }-->
    <!--      "-->
    <!--      >Toggle offcanvas-->
    <!--    </CButton>-->

    <!--    <COffcanvas-->
    <!--      placement="end"-->
    <!--      :visible="visible"-->
    <!--      @hide="-->
    <!--        () => {-->
    <!--          visible = !visible-->
    <!--        }-->
    <!--      "-->
    <!--    >-->
    <!--      <COffcanvasHeader>-->
    <!--        <COffcanvasTitle>Offcanvas</COffcanvasTitle>-->
    <!--        <CCloseButton-->
    <!--          class="text-reset"-->
    <!--          @click="-->
    <!--            () => {-->
    <!--              visible = false-->
    <!--            }-->
    <!--          "-->
    <!--        />-->
    <!--      </COffcanvasHeader>-->
    <!--      <COffcanvasBody>-->
    <!--        Content for the offcanvas goes here. You can place just about any Bootstrap component or-->
    <!--        custom elements here.-->
    <!--      </COffcanvasBody>-->
    <!--    </COffcanvas>-->
  </CRow>
</template>

<style lang="scss" scoped>
.main {
  border-right: 1px solid #ddd !important;
}

.dark-theme .main {
  border-right: 1px solid #333 !important;
}
</style>
