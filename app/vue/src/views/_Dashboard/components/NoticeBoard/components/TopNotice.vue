<script setup lang="ts">
import { inject, type PropType } from 'vue'
import type { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

defineProps({
  post: { type: Object as PropType<Post>, default: null },
})
const userInfo = inject('userInfo')
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>
      <v-badge color="primary" content=" 공지 " offset-x="5" offset-y="-7" />
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        v-if="!post.is_secret || userInfo.is_superuser || userInfo.pk === post.user.pk"
        :to="{ name: `공지 사항 - 보기`, params: { postId: post.pk } }"
      >
        {{ cutString(post.title, 32) }}
      </router-link>
      <span v-else class="text-grey">{{ cutString(post.title, 32) }}</span>
      <v-icon v-if="post.is_secret" icon="mdi-lock" size="sm" class="ml-2 text-grey" />
      <CBadge v-if="post.is_new" color="warning" size="sm" class="ml-2">new</CBadge>
      <CBadge v-if="post.comments?.length" color="warning" size="sm" class="ml-1">
        +{{ post.comments.length }}
      </CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ post.user?.username }}</CTableDataCell>
    <CTableDataCell>{{ timeFormat(post.created ?? '') }}</CTableDataCell>
    <CTableDataCell>{{ post.hit }}</CTableDataCell>
  </CTableRow>
</template>
