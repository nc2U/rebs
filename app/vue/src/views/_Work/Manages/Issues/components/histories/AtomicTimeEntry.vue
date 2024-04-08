<script lang="ts" setup>
import { elapsedTime } from '@/utils/baseMixins'

defineProps({ time: { type: Object, default: () => null } })
</script>

<template>
  <CRow>
    <CCol v-if="time.user">
      <router-link :to="{ name: '사용자 - 보기', params: { userId: time.user.pk } }">
        {{ time.user.username }}
      </router-link>
      이(가)
      <router-link
        :to="{
          name: '(작업내역)',
          params: { projId: 'redmine' },
          query: { from: time.created.substring(0, 10) },
        }"
      >
        {{ elapsedTime(time.created) }}
      </router-link>
      에 추가함
    </CCol>
    <CCol class="text-right pr-3">
      <span>
        <v-icon
          icon="mdi-pencil"
          color="amber"
          class="mr-2 pointer"
          size="18"
          @click="
            $router.push({
              name: '(소요시간) - 편집',
              params: { projId: time.issue.project.slug, timeId: time.pk },
            })
          "
        />
        <v-tooltip activator="parent" location="top">편집</v-tooltip>
      </span>

      <span>
        <v-icon icon="mdi-trash-can" color="grey" size="18" class="pointer" />
        <v-tooltip activator="parent" location="top">삭제</v-tooltip>
      </span>
    </CCol>
  </CRow>
  <v-divider class="mt-0 mb-2" />
  <div class="history pl-4 mb-2">
    <ul>
      <li>작업시간 : {{ time.hours }} 시간</li>
    </ul>
  </div>
  <div class="mb-2">{{ time.comment }}</div>
</template>

<style lang="scss" scoped>
.history {
  color: #7f7f7f;
}

.vue-md-it-wrapper blockquote {
  padding-left: 20px !important;
  border-left: 3px solid #ddd !important;
  font-style: italic;
}
</style>
