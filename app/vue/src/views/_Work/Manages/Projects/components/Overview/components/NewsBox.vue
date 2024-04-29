<script lang="ts" setup>
import { inject, type PropType } from 'vue'
import { type News } from '@/store/types/work'
import { elapsedTime } from '@/utils/baseMixins'

defineProps({ newsList: { type: Array as PropType<News[]>, default: () => [] } })

const isDark = inject('isDark')
</script>

<template>
  <CCard :color="isDark ? '' : 'light'" class="mb-3">
    <CCardBody>
      <CCardSubtitle class="mb-2">
        <v-icon icon="mdi-newspaper" size="sm" color="grey" class="mr-1" />
        최근 뉴스
      </CCardSubtitle>
      <CCardText>
        <div v-for="news in newsList" :key="news.pk">
          <router-link to="">{{ news.title }}</router-link>
          <div>{{ news.summary }}</div>
          <div>
            <span>
              <router-link to=""> {{ news.author?.username }} </router-link>이(가)
              <router-link to="">
                {{ elapsedTime(news.created) }} </router-link
              >에 추가함
            </span>
          </div>
        </div>
      </CCardText>
    </CCardBody>

    <CCardText class="mx-3 mb-2 form-text">
      <router-link to="">모든 뉴스</router-link>
    </CCardText>
  </CCard>
</template>
