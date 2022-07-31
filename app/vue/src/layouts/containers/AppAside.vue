<template>
  <CSidebar
    colorScheme="light"
    selfHiding="xxl"
    size="lg"
    overlaid
    placement="end"
    :visible="asideVisible"
  >
    <CSidebarHeader class="bg-transparent p-0">
      <CCloseButton
        class="float-end p-4"
        @click="$store.commit('toggleAside')"
      />
    </CSidebarHeader>
  </CSidebar>
</template>

<script lang="ts">
import { computed, ref } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'AppAside',
  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  setup() {
    const activeKey = ref(1)

    const updateActiveKey = (key: number) => {
      activeKey.value = key
    }

    const store = useStore()

    return {
      asideVisible: computed(() => store.state.asideVisible),
      activeKey,
      updateActiveKey,
    }
  },
}
</script>
