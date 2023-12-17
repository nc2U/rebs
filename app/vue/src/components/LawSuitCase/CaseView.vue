<script lang="ts" setup>
import { ref, computed, type PropType, watch, onBeforeMount } from 'vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import { useDocument } from '@/store/pinia/document'
import { timeFormat, numFormat } from '@/utils/baseMixins'
import type { SuitCase } from '@/store/types/document'
import { TableSecondary } from '@/utils/cssMixins'

const props = defineProps({
  suitcase: { type: Object as PropType<SuitCase>, required: true },
  viewRoute: { type: String, required: true },
  currPage: { type: Number, required: true },
})

const emit = defineEmits(['cases-renewal', 'link-hit', 'file-hit'])

const prev = ref<number | null>()
const next = ref<number | null>()

const sortName = computed(() => props.suitcase?.proj_name || '본사')
const sortDesc = computed(() => props.suitcase.sort_desc)
const levelDesc = computed(() => props.suitcase.level_desc)

const docStore = useDocument()
const getCaseNav = computed(() => docStore.getCaseNav)

const getPrev = (pk: number) => getCaseNav.value.filter(c => c.pk === pk).map(c => c.prev_pk)[0]
const getNext = (pk: number) => getCaseNav.value.filter(c => c.pk === pk).map(c => c.next_pk)[0]

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

const toDownload = () => window.open(`excel/suitcase/?pk=${route.params.caseId}`, 'blank')

const route = useRoute()

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
      description: `#공지사항 #${props.suitcase?.case_number}`,
      imageUrl: 'https://brdnc.co.kr/static/dist/img/icons/ms-icon-310x310.png',
      link: {
        // [내 애플리케이션] > [플랫폼] 에서 등록한 사이트 도메인과 일치해야 함
        mobileWebUrl: sendUrl,
        webUrl: sendUrl,
      },
    },
    // social: {
    //   // likeCount: props.suitcase.like,
    //   // commentCount: props.suitcase.comments?.length ?? 0,
    //   // sharedCount: 45,
    // },
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

const toScrape = () => alert('스크랩 기능 중비중!')
const toBlame = () => alert('신고 기능 준비중!')

const toDelete = () => alert('준비중!')

watch(
  () => getCaseNav.value,
  () => {
    const caseId = Number(route.params.caseId)
    if (caseId) {
      prev.value = getPrev(caseId)
      next.value = getNext(caseId)
    }
  },
)

onBeforeRouteUpdate((to, from) => {
  const fromCaseId = from.params.caseId ? Number(from.params.caseId) : null
  const toCaseId = to.params.caseId ? Number(to.params.caseId) : null

  const last = getCaseNav.value.length - 1
  const getLast = getCaseNav.value[last]
  if (toCaseId && getLast.pk === fromCaseId && getLast.prev_pk === toCaseId)
    // 다음 페이지 목록으로
    emit('cases-renewal', props.currPage + 1)

  const getFirst = getCaseNav.value[0]
  if (toCaseId && getFirst.pk === fromCaseId && getFirst.next_pk === toCaseId)
    // 이전 페이지 목록으로
    emit('cases-renewal', props.currPage - 1)

  if (toCaseId) {
    prev.value = getPrev(toCaseId)
    next.value = getNext(toCaseId)
  }
})

onBeforeMount(() => {
  const caseId = Number(route.params.caseId)
  if (caseId) {
    prev.value = getPrev(caseId)
    next.value = getNext(caseId)
  }
})
</script>

<template>
  <div v-if="suitcase" class="m-0 p-0">
    <CRow class="mt-5">
      <CCol md="8">
        <h5>
          {{ suitcase.court_desc || suitcase.other_agency }}
          <v-icon icon="mdi-chevron-double-right" size="xs" />
          {{ suitcase.case_number }}
          <v-icon icon="mdi-chevron-double-right" size="xs" />
          {{ suitcase.case_name }}
        </h5>
      </CCol>
      <CCol class="pt-1 text-right">
        <span>[{{ sortName }}] [{{ sortDesc }}/{{ levelDesc }}]</span>
      </CCol>
    </CRow>

    <hr />

    <CRow class="text-blue-grey">
      <CCol>
        <small class="mr-3">작성자 : {{ suitcase.user }}</small>
        <small class="mr-3 text-btn" @click="toPrint">
          <v-icon icon="mdi-printer" size="small" />
          <span class="ml-2">프린트</span>
        </small>
        <small class="mr-3 text-btn" @click="toDownload">
          <v-icon icon="mdi-microsoft-excel" size="small" />
          <span class="ml-2">다운로드</span>
        </small>
      </CCol>

      <CCol class="text-right" md="3">
        <small>
          <v-icon icon="mdi-calendar-clock" size="small" />
          <span class="ml-2">{{ timeFormat(suitcase.created ?? '') }}</span>
        </small>
      </CCol>
    </CRow>

    <CRow class="justify-content-center" id="print-area">
      <CCol md="10 py-5">
        <CTable bordered responsive align="middle">
          <colgroup>
            <col style="width: 25%" />
            <col style="width: 30%" />
            <col style="width: 15%" />
            <col style="width: 30%" />
          </colgroup>
          <CTableHead>
            <CTableRow class="text-center" :color="TableSecondary">
              <CTableHeaderCell scope="col" class="w-25"> 구 분</CTableHeaderCell>
              <CTableHeaderCell scope="col" colspan="4">내 용</CTableHeaderCell>
            </CTableRow>
          </CTableHead>

          <CTableBody>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                사건 번호
              </CTableHeaderCell>
              <CTableDataCell colspan="4">{{ suitcase.case_number }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                사건 명
              </CTableHeaderCell>
              <CTableDataCell colspan="4">{{ suitcase.case_name }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                유 형
              </CTableHeaderCell>
              <CTableDataCell colspan="4">{{ suitcase.sort_desc }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                심 급
              </CTableHeaderCell>
              <CTableDataCell colspan="4">{{ suitcase.level_desc }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                관련 사건
              </CTableHeaderCell>
              <CTableDataCell colspan="4">
                <router-link
                  :to="{
                    name: `${viewRoute} - 보기`,
                    params: { caseId: `${suitcase.related_case}` },
                  }"
                >
                  {{ suitcase.related_case_name }}
                </router-link>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                관할 법원
              </CTableHeaderCell>
              <CTableDataCell colspan="4">{{ suitcase.court_desc }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                기타 처리기관
              </CTableHeaderCell>
              <CTableDataCell colspan="4">{{ suitcase.other_agency }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                원고 (채권자)
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.plaintiff }}</CTableDataCell>

              <CTableHeaderCell class="text-center" :color="TableSecondary">
                피고 (채무자)
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.defendant }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                원고측 대리인
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.plaintiff_attorney }}</CTableDataCell>

              <CTableHeaderCell class="text-center" :color="TableSecondary">
                피고측 대리인
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.defendant_attorney }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                원고 소가(원)
              </CTableHeaderCell>
              <CTableDataCell>{{ numFormat(suitcase.plaintiff_case_price ?? 0) }}</CTableDataCell>

              <CTableHeaderCell class="text-center" :color="TableSecondary">
                피고 소가(원)
              </CTableHeaderCell>
              <CTableDataCell>{{ numFormat(suitcase.defendant_case_price ?? 0) }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                제3 채무자
              </CTableHeaderCell>
              <CTableDataCell colspan="4">{{ suitcase.related_debtor }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                사건 개시일
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.case_start_date }}</CTableDataCell>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                사건 종결일
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.case_end_date }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                개요 및 경과
              </CTableHeaderCell>
              <CTableDataCell colspan="4">{{ suitcase.summary }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                사건 관련 문서
              </CTableHeaderCell>
              <CTableDataCell colspan="4">
                <h6 v-if="suitcase.links?.length">링크</h6>
                <table>
                  <tr v-for="(sc, i) in suitcase.links" :key="i" class="mb-1">
                    <td style="width: 15px">▪</td>
                    <td style="width: 100px" class="pl-3 pb-2">
                      <v-badge
                        :content="sc.category.name"
                        :color="sc.category.color ?? 'secondary'"
                      />
                    </td>
                    <td>
                      <a :href="sc.link" target="_blank" @click="linkHitUp(sc.pk)">
                        {{ sc.link }}
                      </a>
                    </td>
                  </tr>
                </table>
                <h6 v-if="suitcase.files?.length">파일</h6>
                <table>
                  <tr v-for="(sc, i) in suitcase.files" :key="i" class="mb-1">
                    <td style="width: 15px">▪</td>
                    <td style="width: 100px" class="pl-3 pb-2">
                      <v-badge
                        :content="sc.category.name"
                        :color="sc.category.color ?? 'secondary'"
                      />
                    </td>
                    <td>
                      <a :href="sc.file" target="_blank" @click="fileHitUp(sc.pk)">
                        {{ sc.file.split('/').pop() }}
                      </a>
                    </td>
                  </tr>
                </table>
              </CTableDataCell>
            </CTableRow>
          </CTableBody>
        </CTable>
      </CCol>
    </CRow>

    <CRow class="mt-2 px-3">
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
        <v-btn variant="tonal" size="small" :rounded="0" class="mr-1" @click="toScrape">
          스크랩
        </v-btn>
        <v-btn variant="tonal" size="small" :rounded="0" @click="toBlame"> 신고</v-btn>
      </CCol>
    </CRow>

    <hr />

    <CRow class="py-4">
      <CCol>
        <CButtonGroup role="group">
          <CButton
            color="success"
            @click="
              $router.push({
                name: `${viewRoute} - 수정`,
                params: { caseId: suitcase.pk },
              })
            "
          >
            수정
          </CButton>
          <CButton color="danger" @click="toDelete">삭제</CButton>
          <CButton color="light" @click="$router.push({ name: `${viewRoute}` })"> 목록</CButton>
          <CButton
            color="light"
            :disabled="!prev"
            @click="
              $router.push({
                name: `${viewRoute} - 보기`,
                params: { caseId: prev },
              })
            "
          >
            이전
          </CButton>
          <CButton
            color="light"
            :disabled="!next"
            @click="
              $router.push({
                name: `${viewRoute} - 보기`,
                params: { caseId: next },
              })
            "
          >
            다음
          </CButton>
        </CButtonGroup>
      </CCol>
      <CCol class="text-right">
        <CButton color="primary" @click="$router.push({ name: `${viewRoute} - 작성` })">
          신규등록
        </CButton>
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