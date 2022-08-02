<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { CSidebar } from '@coreui/vue'

// const activeKey = ref(1)

// const updateActiveKey = (key: number) => {
//   activeKey.value = key
// }

const store = useStore()

const asideVisible = computed(() => store.state.asideVisible)
</script>

<template>
  <CSidebar
    self-hiding="xxl"
    size="lg"
    overlaid
    position="end"
    :visible="asideVisible"
    class="text-body"
  >
    <CSidebarHeader class="bg-transparent p-0">
      <CCloseButton
        class="float-end p-4"
        @click="$store.commit('toggleAside')"
      />
    </CSidebarHeader>
    <span class="text-body">asdasdfasdf</span>
  </CSidebar>
</template>
