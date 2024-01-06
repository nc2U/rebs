<script lang="ts" setup>
import { type PropType } from 'vue'
import { timeFormat } from '@/utils/baseMixins'
import type { TrashPost } from '@/store/types/document'
import sanitizeHtml from 'sanitize-html'

const props = defineProps({
  category: { type: Number, default: undefined },
  post: { type: Object as PropType<TrashPost>, default: null },
  viewRoute: { type: String, required: true },
  currPage: { type: Number, required: true },
})

const emit = defineEmits(['restore-post'])

const restorePost = () => emit('restore-post', props.post.pk)
</script>

<template>
  <div v-if="post" class="m-0 p-0">
    <CRow class="mt-2">
      <CCol md="8">
        <h6>[{{ post.board_name }}]</h6>
      </CCol>
    </CRow>

    <CRow class="mt-3">
      <CCol md="8">
        <h5>{{ post.title }}</h5>
      </CCol>

      <!--      <CCol class="pt-1 pr-3 text-right">-->
      <!--        <span>[{{ post.board_name }}]</span>-->
      <!--      </CCol>-->
    </CRow>

    <v-divider />

    <CRow class="text-blue-grey mb-5">
      <CCol>
        <small class="mr-3">작성자 : {{ post.user }}</small>
      </CCol>

      <CCol class="text-right" md="3">
        <small>
          <v-icon icon="mdi-delete-clock-outline" size="small" />
          <span class="ml-2">{{ timeFormat(post?.deleted ?? '') }}</span>
        </small>
      </CCol>
    </CRow>

    <CRow class="my-5 p-3" id="print-area">
      <CCol>
        <div v-html="sanitizeHtml(post.content)" />
      </CCol>
    </CRow>

    <v-divider />

    <CRow class="py-2">
      <CCol class="text-right">
        <CButtonGroup role="group">
          <CButton color="secondary" @click="$router.push({ name: `${viewRoute}` })">
            목록으로
          </CButton>
          <CButton color="success" @click="restorePost"> 복원하기</CButton>
        </CButtonGroup>
      </CCol>
    </CRow>
  </div>
</template>

<style lang="scss" scoped>
.social i {
  cursor: pointer;
}

.social i:hover {
  color: darkslateblue;
}
</style>
