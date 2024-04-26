<script lang="ts" setup>
defineProps({
  issuePk: { type: Number, required: true },
  subIssues: { type: Array, default: () => [] },
})
</script>

<template>
  <span class="title mr-2">
    <router-link :to="{ name: '(업무)', query: { parent: issuePk } }">
      {{ subIssues.length }}
    </router-link>
  </span>
  <span class="form-text">
    (<span v-if="subIssues.filter(i => !i.closed).length">
      <router-link :to="{ name: '(업무)', query: { parent: issuePk, status: 'open' } }">
        {{ subIssues.filter(i => !i.closed).length }} 건 진행 중
      </router-link>
    </span>
    <span>모두 완료</span>
    -
    <span v-if="subIssues.filter(i => i.closed).length">
      <router-link :to="{ name: '(업무)', query: { parent: issuePk, status: 'closed' } }">
        {{ subIssues.filter(i => i.closed).length }} 건 완료
      </router-link>
    </span>
    <span v-else>모두 미완료</span>)
  </span>
</template>
