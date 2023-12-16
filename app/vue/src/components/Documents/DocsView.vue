<script lang="ts" setup>
import { computed, onBeforeMount, onMounted, type PropType, ref, watch } from 'vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import { useDocument } from '@/store/pinia/document'
import { cutString, timeFormat } from '@/utils/baseMixins'
import { type Post } from '@/store/types/document'
import sanitizeHtml from 'sanitize-html'

const props = defineProps({
  boardNum: { type: Number, default: 2 },
  heatedPage: { type: Array as PropType<number[]>, default: () => [] },
  reOrder: { type: Boolean, default: false },
  category: { type: Number, default: undefined },
  post: { type: Object as PropType<Post>, default: null },
  likePosts: { type: Array as PropType<number[]>, default: () => [] },
  viewRoute: { type: String, required: true },
  currPage: { type: Number, required: true },
})

const emit = defineEmits(['to-like', 'post-hit', 'link-hit', 'file-hit', 'posts-renewal'])

const prev = ref<number | null>()
const next = ref<number | null>()

const sortName = computed(() => props.post?.proj_name || '본사 문서')
const postId = computed(() => Number(route.params.postId))

const docStore = useDocument()
const getPostNav = computed(() => docStore.getPostNav)

const getPrev = (pk: number) => getPostNav.value.filter(p => p.pk === pk).map(p => p.prev_pk)[0]
const getNext = (pk: number) => getPostNav.value.filter(p => p.pk === pk).map(p => p.next_pk)[0]

const isLike = computed(() => props.likePosts.includes(props.post.pk ?? 0))
const toLike = () => emit('to-like', props.post.pk)

const linkHitUp = async (pk: number) => emit('link-hit', pk)
const fileHitUp = async (pk: number) => emit('file-hit', pk)

const toPrint = () => {
  // Clone the specific area to be printed
  const printContent: any = document.getElementById('print-area')?.cloneNode(true)

  // Create a new window for printing
  const printWindow = window.open('', '_blank')
  if (printWindow) {
    printWindow.document.open()

    // Add the cloned content to the new window
    printWindow.document.write('<html><head><title>Print</title></head><body>')
    printWindow.document.write(printContent?.innerHTML)
    printWindow.document.write('</body></html>')

    // Close the document for writing
    printWindow.document.close()

    // Print the new window
    printWindow.print()
    // Close the new window after printing
    printWindow.close()
  }
}
const toSocial = () => alert('준비중!')
const toDelete = () => alert('준비중!')

const getFileName = (file: string) => {
  if (file) return decodeURI(file.split('/').slice(-1)[0])
  else return
}

const route = useRoute()

watch(
  () => getPostNav.value,
  () => {
    if (postId.value) {
      prev.value = getPrev(postId.value)
      next.value = getNext(postId.value)
    }
  },
)

onBeforeRouteUpdate((to, from) => {
  const toRoute = (to.name ?? '') as string
  if (toRoute.includes('보기')) {
    const fromPostId = from.params.postId ? Number(from.params.postId) : null
    const toPostId = to.params.postId ? Number(to.params.postId) : null

    const last = getPostNav.value.length - 1
    const getLast = getPostNav.value[last]
    if (toPostId && getLast.pk === fromPostId && getLast.prev_pk === toPostId)
      // 다음 페이지 목록으로
      emit('posts-renewal', props.currPage + 1)

    const getFirst = getPostNav.value[0]
    if (toPostId && getFirst.pk === fromPostId && getFirst.next_pk === toPostId)
      // 이전 페이지 목록으로
      emit('posts-renewal', props.currPage - 1)

    if (toPostId) {
      prev.value = getPrev(toPostId)
      next.value = getNext(toPostId)
    }
  }
})

onBeforeMount(() => {
  if (postId.value) {
    prev.value = getPrev(postId.value)
    next.value = getNext(postId.value)
  }
})

onMounted(() => {
  if (postId.value && !props.heatedPage?.includes(postId.value)) {
    emit('post-hit', postId.value)
  }
})
</script>

<template>
  <div v-if="post" class="m-0 p-0">
    <CRow class="mt-5">
      <CCol md="8">
        <h5>{{ post.title }}</h5>
      </CCol>
      <CCol v-if="post.cate_name" class="pt-1 text-right">
        <span>[{{ sortName }}] [{{ post.cate_name }}]</span>
      </CCol>
    </CRow>

    <hr />

    <CRow class="text-blue-grey">
      <CCol>
        <small class="mr-3">작성자 : {{ post.user }}</small>
        <small class="mr-2">
          <v-icon icon="mdi-comment-text-multiple" size="sm" />
          <span class="ml-1">{{ post.comments?.length || 0 }}</span>
        </small>
        <small class="mr-2">
          <v-icon icon="mdi-eye" size="sm" />
          <span class="ml-1">{{ post.hit }}</span>
        </small>
        <small class="mr-2">
          <v-icon icon="mdi-heart" size="sm" />
          <span class="ml-1">{{ post.like }}</span>
        </small>
        <small class="mr-2 text-btn" @click="toPrint">
          <v-icon icon="mdi-printer" size="sm" />
          <span class="ml-1">프린트</span>
        </small>
      </CCol>

      <CCol class="text-right" md="3">
        <small>
          <v-icon icon="mdi-calendar-clock" size="small" />
          <span class="ml-2">{{ timeFormat(post.created ?? '') }}</span>
        </small>
      </CCol>
    </CRow>

    <CRow class="mt-5 py-2 justify-content-between">
      <CCol md="7" lg="6" xl="5">
        <table v-if="boardNum !== 1 && post.execution_date" class="table table-bordered mt-2 mb-3">
          <tbody>
            <tr v-if="post.lawsuit">
              <td class="p-2 bg-blue-grey-lighten-4 text-center">관련사건</td>
              <td class="p-2">
                <router-link
                  :to="{ name: '현장 소송 사건 - 보기', params: { caseId: post.lawsuit } }"
                >
                  {{ post.lawsuit_name }}
                </router-link>
              </td>
            </tr>
            <tr>
              <td class="p-2 bg-blue-grey-lighten-4 text-center">발행일자</td>
              <td class="p-2">{{ post.execution_date }}</td>
            </tr>
          </tbody>
        </table>
      </CCol>

      <CCol md="7" lg="6" xl="5">
        <CRow v-if="!!post.links && post.links.length" class="mb-3">
          <CCol>
            <CListGroup>
              <CListGroupItem>Link</CListGroupItem>
              <CListGroupItem
                v-for="l in post.links"
                :key="l.pk"
                class="d-flex justify-content-between align-items-center"
              >
                <a :href="l.link" target="_blank" @click="linkHitUp(l.pk as number)">
                  {{ cutString(l.link, 45) }}
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

        <CRow v-if="post.files && post.files.length">
          <CCol>
            <CListGroup>
              <CListGroupItem>File</CListGroupItem>
              <CListGroupItem
                v-for="f in post.files"
                :key="f.pk"
                class="d-flex justify-content-between align-items-center"
              >
                <a :href="f.file" target="_blank" @click="fileHitUp(f.pk as number)">
                  {{ cutString(getFileName(f.file ?? ''), 45) }}
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

    <CRow class="my-5 p-3" id="print-area">
      <CCol>
        <div v-html="sanitizeHtml(post.content)" />
      </CCol>
    </CRow>

    <CRow class="py-3">
      <CCol class="text-center">
        <v-btn @click="toLike" variant="outlined" icon="true" color="grey" size="small">
          <v-icon :icon="isLike ? 'mdi-heart' : 'mdi-heart-outline'" size="small" />
          <v-tooltip activator="parent" location="end">좋아요</v-tooltip>
        </v-btn>
      </CCol>
    </CRow>

    <CRow class="my-3 px-3">
      <CCol class="text-grey-darken-1 pt-2 social">
        <v-icon icon="mdi-facebook" class="mr-2" @click="toSocial" />
        <v-icon icon="mdi-twitter" class="mr-2" @click="toSocial" />
        <v-icon icon="mdi-instagram" class="mr-2" @click="toSocial" />
      </CCol>
      <CCol class="text-right">
        <v-btn variant="tonal" size="small" :rounded="0" class="mr-1" @click="toSocial">
          스크랩
        </v-btn>
        <v-btn variant="tonal" size="small" :rounded="0" @click="toSocial"> 신고</v-btn>
      </CCol>
    </CRow>

    <hr />

    <CRow class="py-2">
      <CCol>
        <CButtonGroup role="group" class="mr-3">
          <CButton
            color="light"
            :disabled="!prev || reOrder"
            @click="
              $router.push({
                name: `${viewRoute} - 보기`,
                params: { postId: prev },
              })
            "
          >
            이전글
          </CButton>
          <CButton
            color="light"
            :disabled="!next || reOrder"
            @click="
              $router.push({
                name: `${viewRoute} - 보기`,
                params: { postId: next },
              })
            "
          >
            다음글
          </CButton>
        </CButtonGroup>
      </CCol>
      <CCol class="text-right">
        <CButtonGroup role="group">
          <CButton
            color="success"
            @click="
              $router.push({
                name: `${viewRoute} - 수정`,
                params: { postId: post.pk },
              })
            "
          >
            수정
          </CButton>
          <CButton color="danger" @click="toDelete">삭제</CButton>
          <CButton color="secondary" @click="$router.push({ name: `${viewRoute}` })"> 목록</CButton>
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
