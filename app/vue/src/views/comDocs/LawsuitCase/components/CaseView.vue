<script lang="ts" setup>
import { computed, onBeforeMount, watch } from 'vue'
import { useDocument } from '@/store/pinia/document'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import { headerSecondary } from '@/utils/cssMixins'

const documentStore = useDocument()
const suitcase = computed(() => documentStore.suitcase)

const fetchSuitCase = (pk: number) => documentStore.fetchSuitCase(pk)

const route = useRoute()

watch(route, val => {
  if (val.params.caseId) fetchSuitCase(Number(val.params.caseId))
  else documentStore.post = null
})

onBeforeMount(() => {
  if (route.params.caseId) fetchSuitCase(Number(route.params.caseId))
})

onBeforeRouteLeave(() => {
  documentStore.suitcase = null
})
</script>

<template>
  <div v-if="suitcase" class="m-0 p-0">
    <CRow class="mt-5">
      <CCol md="8">
        <h5>
          {{ suitcase.court_desc }}
          {{ suitcase.case_number }}
          {{ suitcase.case_name }}
        </h5>
      </CCol>
      <CCol class="pt-1 text-right">
        <!--        <span>[{{ sortName }}] [{{ suitcase.cate_name }}]</span>-->
      </CCol>
    </CRow>

    <hr />

    <CRow class="text-blue-grey">
      <CCol>
        <!--        <small class="mr-3">작성자 : {{ suitcase.user }}</small>-->
        <small class="mr-3">
          <v-icon icon="mdi-comment-text-multiple" size="small" />
          <!--          <span class="ml-2">{{ suitcase.comments.length || 0 }}</span>-->
        </small>
        <small class="mr-3">
          <v-icon icon="mdi-eye" size="small" />
          <!--          <span class="ml-2">{{ suitcase.hit }}</span>-->
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
          <!--          <span class="ml-2">{{ timeFormat(suitcase.created) }}</span>-->
        </small>
      </CCol>
    </CRow>

    <CRow class="justify-content-center">
      <CCol md="10 py-5">
        <CTable bordered responsive align="middle">
          <CTableHead>
            <CTableRow class="text-center" :color="headerSecondary">
              <CTableHeaderCell scope="col" class="w-25">
                구 분
              </CTableHeaderCell>
              <CTableHeaderCell scope="col">내 용</CTableHeaderCell>
            </CTableRow>
          </CTableHead>

          <CTableBody>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                유 형
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.sort_desc }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                심 급
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.level_desc }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                관련사건
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.related_case_name }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                법원명
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.court_desc }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                기타 처리기관
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.other_agency }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                사건번호
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.case_number }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                사건명
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.case_name }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                원고(신청인)
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.plaintiff }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                피고(피신청인)
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.defendant }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                제3채무자
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.related_debtor }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                사건개시일
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.case_start_date }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell class="text-center" :color="headerSecondary">
                개요 및 경과
              </CTableHeaderCell>
              <CTableDataCell>{{ suitcase.summary }}</CTableDataCell>
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
                name: '본사 소송사건 - 보기',
                params: { caseId: getPrev },
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
                name: '본사 소송사건 - 보기',
                params: { caseId: getNext },
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
                name: '본사 소송사건 - 수정',
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
        <CButton color="light" @click="$router.push({ name: '본사 소송사건' })">
          목록으로
        </CButton>
        <CButton
          color="primary"
          @click="$router.push({ name: '본사 소송사건 - 작성' })"
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
