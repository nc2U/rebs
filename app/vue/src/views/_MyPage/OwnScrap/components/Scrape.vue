<script setup lang="ts">
import { ref, computed, type PropType, onBeforeMount } from 'vue'
import type { Scrape as S } from '@/store/types/accounts'
import { cutString, timeFormat } from '@/utils/baseMixins'

const props = defineProps({
  scrape: { type: Object as PropType<S>, default: null },
})

const emit = defineEmits(['patch-title'])

const titleEdit = ref(false)
const scrapeTitle = ref('')

const viewRoute = computed(() => {
  if (props.scrape?.post.board === 1) return '공지 사항'
  if (!!props.scrape?.post.project) {
    if (props.scrape.post.board === 2) return '현장 일반 문서'
    else if (props.scrape.post.board === 3) return '현장 소송 문서'
  } else {
    if (props.scrape?.post.board === 2) return '본사 일반 문서'
    else if (props.scrape?.post.board === 3) return '본사 소송 문서'
  }
  return '공지 사항'
})

const patchTitle = () => {
  emit('patch-title', props.scrape.pk, scrapeTitle.value)
  titleEdit.value = false
}

onBeforeMount(() => {
  if (props.scrape?.title) scrapeTitle.value = props.scrape.title
})
</script>

<template>
  <CTableRow v-if="scrape" class="text-center">
    <CTableDataCell>{{ scrape.pk }}</CTableDataCell>
    <CTableDataCell>
      <router-link :to="{ name: viewRoute }">{{ scrape.post.board_name }}</router-link>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <span v-if="!titleEdit">
        <router-link :to="{ name: `${viewRoute} - 보기`, params: { postId: scrape.post.pk } }">
          {{ cutString(scrape.title || scrape.post.title, 50) }}
        </router-link>
      </span>
      <span v-else>
        <CInputGroup>
          <CFormInput
            v-model="scrapeTitle"
            placeholder="스크랩 제목을 입력하세요"
            aria-label="Alias title"
            :aria-describedby="`alias-title-${scrape.pk}`"
          />
          <CButton @click="patchTitle" type="button" color="info" :id="`alias-title-${scrape.pk}`">
            저장
          </CButton>
        </CInputGroup>
      </span>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(scrape.created ?? '') }}</CTableDataCell>
    <CTableDataCell>
      <v-btn
        @click="titleEdit = !titleEdit"
        density="compact"
        icon="mdi-plus"
        rounded="1"
        size="sm"
        color="success"
      />
    </CTableDataCell>
    <CTableDataCell>
      <v-btn density="compact" icon="mdi-trash-can-outline" size="sm" rounded="1" color="red" />
    </CTableDataCell>
  </CTableRow>
</template>
