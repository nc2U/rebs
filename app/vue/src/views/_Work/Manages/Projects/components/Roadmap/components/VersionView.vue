<script lang="ts" setup>
import { onBeforeMount, type PropType } from 'vue'
import { useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import type { Version } from '@/store/types/work'
import IssueDropDown from '@/views/_Work/Manages/Issues/components/IssueDropDown.vue'

defineProps({ version: { type: Object as PropType<Version>, required: true } })

const emit = defineEmits(['aside-visible'])

const workStore = useWork()

const boxClass = ['primary-box', 'danger-box', 'success-box']

const route = useRoute()
onBeforeMount(() => {
  emit('aside-visible', false)
  workStore.fetchVersion(Number(route.params.verId))
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="title bold mr-2" style="font-size: large">{{ version?.name }}</span>

      <span :class="boxClass[Number(version?.status) - 1]">{{ version?.status_desc }}</span>
    </CCol>
  </CRow>

  <CRow v-if="version?.description" class="mb-2">
    <CCol>{{ version?.description }}</CCol>
  </CRow>

  <template v-if="!version?.issues?.length">
    <div class="form-text mb-3">이 버전에 해당하는 업무 없음</div>
  </template>

  <template v-else>
    <CRow>
      <CCol class="col-sm-10 col-md-8 col-lg-6 col-xl-4 p-0 mx-2">
        <CProgress color="success" :value="50" :style="{ '--cui-border-radius': 0 }">
          50%
        </CProgress>
      </CCol>
    </CRow>
    <CRow class="mb-4">
      <CCol class="form-text">
        <span>
          <router-link to="">6 업무</router-link>
        </span>
        <span>( <router-link to="">5 건 완료</router-link> - </span>
        <span> <router-link to="">한 건 진행 중</router-link>) </span>
      </CCol>
    </CRow>

    <CRow>
      <CCol md="8" class="mb-4">
        <h6>연결된 업무</h6>
        <v-divider class="mb-0" />
        <CTable responsive hover small striped>
          <colgroup>
            <col style="width: 95%" />
            <col style="width: 5%" />
          </colgroup>
          <CTableBody>
            <CTableRow v-for="issue in version.issues" :key="issue.pk">
              <CTableDataCell>
                <span>
                  <router-link
                    :to="{ name: '(업무) - 보기', params: { issueId: issue.pk } }"
                    :class="{ closed: issue.closed }"
                  >
                    기능 #{{ issue.pk }}
                  </router-link>
                </span>
                <span> : {{ issue.subject }}</span>
              </CTableDataCell>
              <CTableDataCell class="text-center p-0">
                <IssueDropDown :issue="issue" />
              </CTableDataCell>
            </CTableRow>
          </CTableBody>
        </CTable>
      </CCol>

      <CCol md="4" class="mb-4">
        <CRow class="mb-2">
          <CCol class="col-4 col-lg-6 col-xl-4">
            <CFormSelect readonly disabled>
              <option>유형</option>
              <option>상태</option>
              <option>우선순위</option>
              <option>저자</option>
              <option>담당자</option>
              <option>범주</option>
            </CFormSelect>
          </CCol>
          <CCol style="padding-top: 6px">별 업무</CCol>
        </CRow>
        <div class="p-2 border">
          <CRow class="my-2">
            <CCol class="col-3 text-right">결함</CCol>
            <CCol class="col-6">
              <CProgress value="10" color="success" />
            </CCol>
            <CCol class="col-3">4/5</CCol>

            <CCol class="col-3 text-right">기능</CCol>
            <CCol class="col-6">
              <CProgress />
            </CCol>
            <CCol class="col-3">1/1</CCol>
          </CRow>
        </div>
      </CCol>
    </CRow>
  </template>
</template>
