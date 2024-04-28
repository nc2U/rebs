<script lang="ts" setup>
import { inject } from 'vue'

defineProps({ projectMemgers: { type: Array, default: () => [] } }, {})

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
