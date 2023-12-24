<script lang="ts" setup>
import {
  computed,
  type ComputedRef,
  inject,
  onBeforeMount,
  onMounted,
  type PropType,
  ref,
  watch,
} from 'vue'
import { onBeforeRouteUpdate, useRoute, useRouter } from 'vue-router'
import { useDocument } from '@/store/pinia/document'
import { cutString, timeFormat } from '@/utils/baseMixins'
import type { User } from '@/store/types/accounts'
import type { Post } from '@/store/types/document'
import sanitizeHtml from 'sanitize-html'
import Comments from '@/components/Comments/Index.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  heatedPage: { type: Array as PropType<number[]>, default: () => [] },
  reOrder: { type: Boolean, default: false },
  category: { type: Number, default: undefined },
  post: { type: Object as PropType<Post>, required: true },
  likePosts: { type: Array as PropType<number[]>, default: () => [] },
  viewRoute: { type: String, required: true },
  currPage: { type: Number, required: true },
  writeAuth: { type: Boolean, default: true },
})

const emit = defineEmits([
  'to-like',
  'post-hit',
  'link-hit',
  'file-hit',
  'post-scrape',
  'posts-renewal',
  'post-delete',
])

const refDelModal = ref()
const refAlertModal = ref()

const userInfo = inject<ComputedRef<User>>('userInfo')
const editAuth = computed(
  () => userInfo?.value?.is_superuser || props.post.user?.pk === userInfo?.value?.pk,
)

const prev = ref<number | null>()
const next = ref<number | null>()

const postId = computed(() => Number(route.params.postId))

const docStore = useDocument()
const commentList = computed(() => docStore.commentList)
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

const [route, router] = [useRoute(), useRouter()]

const sendUrl = `${window.location.host}${route.fullPath}`

const shareFacebook = () => window.open(`https://facebook.com/share/share.php?u=${sendUrl}`)

const shareTwitter = () => window.open(`https://twitter.com/intent/tweet?text=&url=${sendUrl}`)

const shareKakaoTalk = () => {
  // 카카오링크 버튼 생성
  ;(window as any).Kakao.Share.createDefaultButton({
    container: '#kakaotalk-sharing-btn',
    objectType: 'feed',
    content: {
      title: '주식회사 바램디앤씨',
      description: `#공지사항 #${props.post?.title}`,
      imageUrl: 'https://brdnc.co.kr/static/dist/img/icons/ms-icon-310x310.png',
      link: {
        // [내 애플리케이션] > [플랫폼] 에서 등록한 사이트 도메인과 일치해야 함
        mobileWebUrl: sendUrl,
        webUrl: sendUrl,
      },
    },
    social: {
      likeCount: props.post.like,
      commentCount: props.post.comments?.length ?? 0,
      // sharedCount: 45,
    },
    buttons: [
      {
        title: '웹으로 보기',
        link: {
          mobileWebUrl: sendUrl,
          webUrl: sendUrl,
        },
      },
      {
        title: '앱으로 보기',
        link: {
          mobileWebUrl: sendUrl,
          webUrl: sendUrl,
        },
      },
    ],
  })
}

const toScrape = () => {
  if (props.post.is_scraped)
    refAlertModal.value.callModal('', '이미 이 포스트를 스크랩 하였습니다.')
  else emit('post-scrape', props.post.pk)
}
const toBlame = () => alert('신고 기능 준비중!')

const items = ref([
  { title: '복사하기', icon: 'content-copy', func: 'toBlame' },
  { title: '이동하기', icon: 'folder-arrow-right', func: 'toBlame' },
  { title: '카테고리변경', icon: 'tag-multiple', func: 'toBlame' },
  { title: '비밀글로', icon: 'lock', func: 'toBlame' },
  { title: '댓글감춤', icon: 'comment-off', func: 'toBlame' },
  { title: '공지올림', icon: 'bullhorn-variant', func: 'toBlame' },
  { title: '블라인드처리', icon: 'eye-off', func: 'toBlame' },
  { title: '휴지통으로', icon: 'trash-can', func: 'toBlame' },
])

const toManage = (i: number) => alert(`${i} - 관리 기능 준비중!`)

const getFileName = (file: string) => {
  if (file) return decodeURI(file.split('/').slice(-1)[0])
  else return
}

const toEdit = () => {
  if (props.post.comments?.length ?? 0 >= 5)
    refAlertModal.value.callModal('', '5개 이상의 댓글이 달린 게시물은 수정할 수 없습니다.')
  else
    router.push({
      name: `${props.viewRoute} - 수정`,
      params: { postId: props.post?.pk },
    })
}

const deleteConfirm = () => refDelModal.value.callModal()

const toDelete = () => {
  refDelModal.value.close()
  if ((userInfo?.value.is_superuser || props.post.comments?.length) ?? 0 < 5)
    emit('post-delete', props.post.pk)
  else refAlertModal.value.callModal('', '5개 이상의 댓글이 달린 게시물은 삭제할 수 없습니다.')
}

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
  if (userInfo?.value.staffauth && postId.value && !props.heatedPage?.includes(postId.value)) {
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
        <span>[{{ post.cate_name }}]</span>
      </CCol>
    </CRow>

    <v-divider />

    <CRow class="text-blue-grey">
      <CCol>
        <small class="mr-3">작성자 : {{ post.user?.username }}</small>
        <small class="mr-2">
          <v-icon icon="mdi-comment-text-multiple" size="sm" />
          <span class="ml-1">{{ post.comments?.length ?? 0 }}</span>
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
      <CCol md="7" lg="6" xl="5"></CCol>

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
        <a
          id="kakaotalk-sharing-btn"
          href="javascript:void(0)"
          @click="shareKakaoTalk"
          class="mr-2"
        >
          <img
            src="https://developers.kakao.com/assets/img/about/logos/kakaotalksharing/kakaotalk_sharing_btn_medium.png"
            alt="카카오톡 공유 보내기 버튼"
            width="20px;"
          />
        </a>
        <v-icon icon="mdi-facebook" class="mr-2" @click="shareFacebook" />
        <v-icon icon="mdi-twitter" class="mr-2" @click="shareTwitter" />
      </CCol>
      <CCol class="text-right">
        <v-btn
          variant="tonal"
          :color="post.is_scraped ? 'primary' : ''"
          size="small"
          :rounded="0"
          class="mr-1"
          @click="toScrape"
        >
          스크랩 {{ post.is_scraped ? '+1' : '' }}
        </v-btn>
        <v-btn variant="tonal" size="small" :rounded="0" class="mr-1" @click="toBlame"> 신고</v-btn>
        <v-btn
          v-if="userInfo?.is_superuser"
          prepend-icon="mdi-cog"
          variant="tonal"
          size="small"
          :rounded="0"
        >
          관리
          <v-menu activator="parent" open-on-hover>
            <v-list density="compact">
              <v-list-item
                v-for="(item, index) in items"
                :key="index"
                :value="index"
                @click="toManage(index + 1)"
              >
                <v-list-item-title style="font-size: 0.9em">
                  <v-icon :icon="`mdi-${item.icon}`" size="sm" />
                  {{ item.title }}
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-btn>
      </CCol>
    </CRow>

    <v-divider />

    <Comments :post="post.pk as number" :comments="commentList" />

    <v-divider />

    <CRow class="py-2">
      <CCol>
        <CButtonGroup role="group">
          <CButton v-if="editAuth" color="success" :disabled="!writeAuth" @click="toEdit">
            수정
          </CButton>
          <CButton v-if="editAuth" color="danger" :disabled="!writeAuth" @click="deleteConfirm">
            삭제
          </CButton>
          <CButton color="secondary" @click="$router.push({ name: `${viewRoute}` })"> 목록</CButton>
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
            이전
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
            다음
          </CButton>
        </CButtonGroup>
      </CCol>
      <CCol class="text-right">
        <CButton
          color="primary"
          :disabled="!writeAuth"
          @click="$router.push({ name: `${viewRoute} - 작성` })"
        >
          신규등록
        </CButton>
      </CCol>
    </CRow>
  </div>

  <AlertModal ref="refAlertModal" />

  <ConfirmModal ref="refDelModal">
    <template #header>알림</template>
    <template #default>한번 삭제한 자료는 복구할 수 없습니다. 정말 삭제하시겠습니까?</template>
    <template #footer>
      <CButton color="danger" @click="toDelete">삭제</CButton>
    </template>
  </ConfirmModal>
</template>

<style lang="scss" scoped>
.social i {
  cursor: pointer;
}

.social i:hover {
  color: darkslateblue;
}
</style>
