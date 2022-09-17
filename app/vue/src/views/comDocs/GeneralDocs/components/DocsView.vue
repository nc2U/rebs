<script lang="ts" setup="">
import { computed, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { useDocument } from '@/store/pinia/document'
import { timeFormat } from '@/utils/baseMixins'

const route = useRoute()

const documentStore = useDocument()
const post = computed(() => documentStore.post)
const sortName = computed(() => post.value.proj_name || '본사')

const fetchPost = (pk: number) => documentStore.fetchPost(pk)

const toPrint = () => alert('준비중!')

const toSocial = () => alert('준비중!')

onBeforeMount(() => fetchPost(Number(route.params.postId)))
</script>

<template>
  <div v-if="post" class="m-0 p-0">
    <CRow class="mt-5">
      <CCol md="6">
        <h5>{{ post.title }}</h5>
      </CCol>
      <CCol class="pt-1 text-right">
        <span>[{{ sortName }}] [{{ post.cate_name }}]</span>
      </CCol>
    </CRow>

    <hr />

    <CRow class="text-blue-grey">
      <CCol>
        <small class="mr-3">작성자 : {{ post.user }}</small>
        <small class="mr-3">
          <v-icon icon="mdi-comment-text-multiple" size="small" />
          <span class="ml-2">{{ post.comments.length || 0 }}</span>
        </small>
        <small class="mr-3">
          <v-icon icon="mdi-eye" size="small" />
          <span class="ml-2">{{ post.hit }}</span>
        </small>
        <small class="mr-3">
          <v-icon icon="mdi-thumb-up" size="small" />
          <span class="ml-2">{{ post.like }}</span>
        </small>
        <small class="mr-3">
          <v-icon icon="mdi-thumb-down" size="small" />
          <span class="ml-2">{{ post.dislike }}</span>
        </small>
        <small class="mr-3 print" @click="toPrint">
          <v-icon icon="mdi-printer" size="small" />
          <span class="ml-2">프린트</span>
        </small>
      </CCol>

      <CCol class="text-right" md="3">
        <small>
          <v-icon icon="mdi-calendar-clock" size="small" />
          <span class="ml-2">{{ timeFormat(post.created) }}</span>
        </small>
      </CCol>
    </CRow>

    <CRow class="mt-5 py-2">
      <CCol md="5" lg="4" xl="3">
        <table class="table table-bordered mt-2 mb-3">
          <tbody>
            <tr class="text-center">
              <td class="p-2 bg-blue-grey-lighten-4">문서 시행일자</td>
              <td class="p-2">{{ post.execution_date }}</td>
            </tr>
          </tbody>
        </table>
      </CCol>
    </CRow>

    <CRow class="my-5 p-3">
      <CCol>
        <div v-html="post.content" />
      </CCol>
    </CRow>

    <CRow class="py-3">
      <CCol class="text-right pr-1">
        <v-btn variant="outlined" icon="true" color="grey" size="small">
          <v-icon icon="mdi-thumb-up" size="small" />
        </v-btn>
      </CCol>
      <CCol class="pl-1 text-body">
        <v-btn variant="outlined" icon="true" color="grey" size="small">
          <v-icon icon="mdi-thumb-down" size="small" />
        </v-btn>
      </CCol>
    </CRow>

    <CRow class="mt-2 px-3">
      <CCol class="text-grey-darken-1 pt-2 social">
        <v-icon icon="mdi-facebook" class="mr-2" @click="toSocial" />
        <v-icon icon="mdi-twitter" class="mr-2" @click="toSocial" />
        <v-icon icon="mdi-instagram" class="mr-2" @click="toSocial" />
      </CCol>
      <CCol class="text-right">
        <v-btn variant="tonal" class="mr-1">스크랩</v-btn>
        <v-btn variant="tonal">신고</v-btn>
      </CCol>
    </CRow>

    <hr />

    <CRow class="py-4">
      <CCol>
        <CButtonGroup role="group" aria-label="Vertical button group">
          <!--          <CButton color="light">목록</CButton>-->
          <CButton color="success">수정</CButton>
          <CButton color="danger">삭제</CButton>
          <CButton color="light">이전글</CButton>
          <CButton color="light">다음글</CButton>
        </CButtonGroup>
      </CCol>
      <CCol class="text-right">
        <CButton color="light" @click="$router.push({ name: '본사 일반문서' })">
          목록으로
        </CButton>
        <CButton
          color="primary"
          @click="$router.push({ name: '본사 일반문서 - 작성' })"
        >
          등록하기
        </CButton>
      </CCol>
    </CRow>
  </div>
</template>

<style lang="scss" scoped>
.print {
  cursor: pointer;
}

.print:hover {
  color: darkslateblue;
}

.social i {
  cursor: pointer;
}

.social i:hover {
  color: darkslateblue;
}
</style>
