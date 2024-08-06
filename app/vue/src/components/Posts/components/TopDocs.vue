<script setup lang="ts">
import { computed, type ComputedRef, inject, type PropType } from 'vue'
import type { User } from '@/store/types/accounts'
import type { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

const props = defineProps({
  post: { type: Object as PropType<Post>, default: null },
  viewRoute: { type: String, required: true },
  isLawsuit: { type: Boolean, default: false },
})

const userInfo = inject<ComputedRef<User>>('userInfo')

const sortName = computed(() => props.post?.proj_name || '본사 문서')
const sortColor = computed(() => (props.post?.project ? 'success' : 'info'))
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>
      <v-badge color="primary" content=" 공지 " offset-x="5" offset-y="-7" />
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <v-badge :color="sortColor" :content="sortName" offset-x="-5" offset-y="-7" />
    </CTableDataCell>
    <CTableDataCell>{{ post.execution_date }}</CTableDataCell>
    <CTableDataCell v-if="isLawsuit" class="text-left">
      {{ cutString(post.lawsuit_name ?? '', 26) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        v-if="!post.is_secret || userInfo?.is_superuser || userInfo?.pk === post.user?.pk"
        :to="{ name: `${viewRoute} - 보기`, params: { postId: post.pk } }"
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
