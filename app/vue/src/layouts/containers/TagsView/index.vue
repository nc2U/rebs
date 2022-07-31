<script lang="ts" setup>
import { ref } from 'vue'

const msg = ref('TagsView')
const test = () => alert('aa')
</script>

<template>
  <v-sheet max-width="100%" class="my-2">
    <v-slide-group show-arrows>
      <v-slide-group-item
        v-for="n in 9"
        :key="n"
        v-slot="{ isSelected, toggle }"
      >
        <v-btn
          class="mx-1 my-0 text-gray"
          size="x-small"
          :border="true"
          :rounded="0"
          :color="isSelected ? 'success' : undefined"
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
</style>
