<script lang="ts" setup>
import { computed, onBeforeMount, onMounted, watch } from 'vue'
import { timeFormat } from '@/utils/baseMixins'
import { PostFilter, useDocument } from '@/store/pinia/document'
import { onBeforeRouteLeave, useRoute } from 'vue-router'

const props = defineProps({ category: { type: Number, default: undefined } })
const emit = defineEmits(['post-hit', 'link-hit', 'file-hit'])

const documentStore = useDocument()
const post = computed(() => documentStore.post)
const getPrev = computed(() => documentStore.getPrev)
const getNext = computed(() => documentStore.getNext)

const sortName = computed(() => post.value?.proj_name || '본사')

const fetchPost = (pk: number) => documentStore.fetchPost(pk)
const fetchLink = (pk: number) => documentStore.fetchLink(pk)
const fetchFile = (pk: number) => documentStore.fetchFile(pk)
const fetchPostList = (payload: PostFilter) =>
  documentStore.fetchPostList(payload)

const toPrint = () => alert('준비중!')
const toSocial = () => alert('준비중!')
const toDelete = () => alert('준비중!')

const linkHitUp = async (pk: number) => {
  const link = await fetchLink(pk)
  link.hit = link.hit + 1
  emit('link-hit', link)
}

const fileHitUp = async (pk: number) => {
  const file = await fetchFile(pk)
  const hit = file.hit + 1
  emit('file-hit', { pk, hit })
}

const getFileName = (file: string) => {
  if (file) return decodeURI(file.split('/').slice(-1)[0])
  else return
}

const route = useRoute()

watch(route, val => {
  if (val.params.postId) fetchPost(Number(val.params.postId))
  else documentStore.post = null
})

onBeforeMount(() => {
  if (route.params.postId) fetchPost(Number(route.params.postId))

  setTimeout(() => {
    if (post.value)
      emit('post-hit', { pk: post.value.pk, hit: post.value.hit + 1 })
  }, 500)
})

onBeforeRouteLeave(() => {
  documentStore.post = null
})
</script>

<template>
  <div v-if="post" class="m-0 p-0">
    <CRow class="mt-5">
      <CCol md="8">
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
          <span class="ml-2">{{ 0 }}</span>
        </small>
        <small class="mr-3">
          <v-icon icon="mdi-thumb-down" size="small" />
          <span class="ml-2">{{ 0 }}</span>
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

    <CRow class="mt-5 py-2 justify-content-between">
      <CCol md="5" lg="4" xl="3">
        <!--        <table class="table table-bordered mt-2 mb-3">-->
        <!--          <tbody>-->
        <!--            <tr class="text-center">-->
        <!--              <td class="p-2 bg-blue-grey-lighten-4">문서 시행일자</td>-->
        <!--              <td class="p-2">{{ post.execution_date }}</td>-->
        <!--            </tr>-->
        <!--          </tbody>-->
        <!--        </table>-->
      </CCol>

      <CCol md="6">
        <CRow v-if="post.links.length" class="mb-3">
          <CCol>
            <CListGroup>
              <CListGroupItem>Link</CListGroupItem>
              <CListGroupItem
                v-for="l in post.links"
                :key="l.pk"
                class="d-flex justify-content-between align-items-center"
              >
                <a :href="l.link" target="_blank" @click="linkHitUp(l.pk)">
                  {{ l.link }}
                </a>
                <small>
                  조회 수 :
                  <CBadge color="info" shape="rounded-pill">
                    {{ l.hit }}
                  </CBadge>
                </small>
              </CListGroupItem>
            </CListGroup>
          </CCol>
        </CRow>

        <CRow v-if="post.files.length">
          <CCol>
            <CListGroup>
              <CListGroupItem>File</CListGroupItem>
              <CListGroupItem
                v-for="f in post.files"
                :key="f.pk"
                class="d-flex justify-content-between align-items-center"
              >
                <a :href="f.file" target="_blank" @click="fileHitUp(f.pk)">
                  {{ getFileName(f.file) }}
                </a>
                <small>
                  다운로드 :
                  <CBadge color="success" shape="rounded-pill">
                    {{ f.hit }}
                  </CBadge>
                </small>
              </CListGroupItem>
            </CListGroup>
          </CCol>
        </CRow>
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
        <v-btn
          variant="tonal"
          size="small"
          :rounded="0"
          class="mr-1"
          @click="toSocial"
        >
          스크랩
        </v-btn>
        <v-btn variant="tonal" size="small" :rounded="0" @click="toSocial">
          신고
        </v-btn>
      </CCol>
    </CRow>

    <hr />

    <CRow class="py-4">
      <CCol>
        <CButtonGroup role="group" class="mr-3">
          <CButton
            color="light"
            :disabled="!getPrev"
            @click="
              $router.push({
                name: '본사 소송문서 - 보기',
                params: { postId: getPrev },
              })
            "
          >
            이전글
          </CButton>
          <CButton
            color="light"
            :disabled="!getNext"
            @click="
              $router.push({
                name: '본사 소송문서 - 보기',
                params: { postId: getNext },
              })
            "
          >
            다음글
          </CButton>
        </CButtonGroup>

        <CButtonGroup role="group">
          <CButton
            color="success"
            @click="
              $router.push({
                name: '본사 소송문서 - 수정',
                params: { postId: post.pk },
              })
            "
          >
            수정
          </CButton>
          <CButton color="danger" @click="toDelete">삭제</CButton>
        </CButtonGroup>
      </CCol>
      <CCol class="text-right">
        <CButton color="light" @click="$router.push({ name: '본사 소송문서' })">
          목록으로
        </CButton>
        <CButton
          color="primary"
          @click="$router.push({ name: '본사 소송문서 - 작성' })"
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
