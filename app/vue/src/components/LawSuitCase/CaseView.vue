<script lang="ts" setup>
import { ref, computed, type PropType, watch, onBeforeMount } from 'vue'
import { timeFormat } from '@/utils/baseMixins'
import { TableSecondary } from '@/utils/cssMixins'
import { type SuitCase } from '@/store/types/document'
import { useDocument } from '@/store/pinia/document'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'

const props = defineProps({
  suitcase: { type: Object as PropType<SuitCase>, required: true },
  viewRoute: { type: String, required: true },
  currPage: { type: Number, required: true },
})

const emit = defineEmits(['cases-renewal'])

const prev = ref<number | null>()
const next = ref<number | null>()

const sortName = computed(() => props.suitcase?.proj_name || '본사')
const sortDesc = computed(() => props.suitcase.sort_desc)
const levelDesc = computed(() => props.suitcase.level_desc)

const docStore = useDocument()
const getCaseNav = computed(() => docStore.getCaseNav)

const getPrev = (pk: number) => getCaseNav.value.filter(c => c.pk === pk).map(c => c.prev_pk)[0]
const getNext = (pk: number) => getCaseNav.value.filter(c => c.pk === pk).map(c => c.next_pk)[0]

const toPrint = () => alert('준비중!')
const toSocial = () => alert('준비중!')
const toDelete = () => alert('준비중!')

const route = useRoute()

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
        <small class="mr-3 print" @click="toPrint">
          <v-icon icon="mdi-printer" size="small" />
          <span class="ml-2">프린트</span>
        </small>
      </CCol>

      <CCol class="text-right" md="3">
        <small>
          <v-icon icon="mdi-calendar-clock" size="small" />
          <span class="ml-2">{{ timeFormat(suitcase.created ?? '') }}</span>
        </small>
      </CCol>
    </CRow>

    <CRow class="justify-content-center">
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
                원고 (채권자)
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.plaintiff }}</CTableDataCell>

              <CTableHeaderCell class="text-center" :color="TableSecondary">
                원고측 대리인
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.plaintiff_attorney }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="TableSecondary">
                피고 (채무자)
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.defendant }}</CTableDataCell>

              <CTableHeaderCell class="text-center" :color="TableSecondary">
                피고측 대리인
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.defendant_attorney }}</CTableDataCell>
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
          </CTableBody>
        </CTable>
      </CCol>
    </CRow>

    <CRow class="mt-2 px-3">
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

    <CRow class="py-4">
      <CCol>
        <CButtonGroup role="group" class="mr-3">
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
        </CButtonGroup>
      </CCol>
      <CCol class="text-right">
        <CButton color="light" @click="$router.push({ name: `${viewRoute}` })"> 목록으로</CButton>
        <CButton color="primary" @click="$router.push({ name: `${viewRoute} - 작성` })">
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
