<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

const msg = ref('TagsView')
const test = () => alert('aa')

const store = useStore()
const dark = computed(() => store.state.theme === 'dark')
const btnColor = computed(() =>
  store.state.theme === 'dark' ? 'blue-grey' : '',
)
</script>

<template>
  <v-sheet max-width="100%" class="my-2" :class="{ dark }">
    <v-slide-group show-arrows>
      <v-slide-group-item
        v-for="n in 9"
        :key="n"
        v-slot="{ isSelected, toggle }"
      >
        <v-btn
          class="mx-1 my-0 text-body"
          :class="{ darkBtn: dark }"
          size="x-small"
          :border="true"
          :rounded="0"
          :color="isSelected ? 'success' : btnColor"
          @click="toggle"
        >
          <v-icon
            v-if="isSelected"
            icon="mdi-circle"
            size="x-small"
            class="mr-2"
          />
          메인 페이지
          <v-icon
            icon="mdi-close"
            size="x-small"
            class="pa-2 ml-1 close"
            @click="test"
          />
        </v-btn>
      </v-slide-group-item>
    </v-slide-group>
  </v-sheet>
</template>

<style lang="scss" scoped>
.close:hover {
  background: #ccc;
}

.dark {
  background: #181924;
}
</style>
