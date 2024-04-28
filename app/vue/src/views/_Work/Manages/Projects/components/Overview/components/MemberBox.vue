<script lang="ts" setup>
import { inject, type PropType } from 'vue'

defineProps({
  projectMemgers: {
    type: Object as PropType<{ [key: string]: { pk: number; username: string }[] }>,
    default: () => null,
  },
})

const isDark = inject('isDark')
</script>

<template>
  <CCard :color="isDark ? '' : 'light'" class="mb-3">
    <CCardBody>
      <CCardSubtitle>구성원</CCardSubtitle>
      <CCardText>
        <div v-for="(val, key) in projectMemgers" :key="key">
          {{ key }} :

          <span v-for="(u, i) in val" :key="u.pk">
            <router-link :to="{ name: '사용자 - 보기', params: { userId: u.pk } }">
              {{ u.username }}
            </router-link>
            <span v-if="Number(i) + 1 < val.length">, </span>
          </span>
        </div>
      </CCardText>
    </CCardBody>
  </CCard>
</template>
