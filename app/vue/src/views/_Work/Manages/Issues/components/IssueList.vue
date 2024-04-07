<script lang="ts" setup>
import type { PropType } from 'vue'
import type { Issue } from '@/store/types/work'
import { timeFormat } from '@/utils/baseMixins'
import NoData from '@/views/_Work/components/NoData.vue'
import SearchList from '@/views/_Work/Manages/Projects/components/SearchList.vue'

defineProps({
  issueList: { type: Array as PropType<Issue[]>, default: () => [] },
})
</script>

<template>
  <CRow>
    <CRow class="py-2">
      <CCol>
        <h5>업무</h5>
      </CCol>

      <CCol class="text-right">
        <span class="mr-2 form-text">
          <v-icon icon="mdi-plus-circle" color="success" size="sm" />
          <router-link :to="{ name: `${String($route.name)} - 추가` }" class="ml-1">
            새 업무만들기
          </router-link>
        </span>
      </CCol>
    </CRow>

    <SearchList />

    <NoData v-if="!issueList.length" />

    <CCol v-else col="12">
      <v-divider class="mb-0" />
      <CTable striped hover small responsive>
        <colgroup>
          <col style="width: 8%" />
          <col v-if="!$route.params.projId" style="width: 16%" />
          <col style="width: 8%" />
          <col style="width: 8%" />
          <col style="width: 8%" />
          <col style="width: 20%" />
          <col style="width: 12%" />
          <col style="width: 15%" />
          <col style="width: 5%" />
        </colgroup>
        <CTableHead>
          <CTableRow class="text-center">
            <CTableHeaderCell scope="col">#</CTableHeaderCell>
            <CTableHeaderCell v-if="!$route.params.projId" scope="col">프로젝트</CTableHeaderCell>
            <CTableHeaderCell scope="col">유형</CTableHeaderCell>
            <CTableHeaderCell scope="col">상태</CTableHeaderCell>
            <CTableHeaderCell scope="col">우선순위</CTableHeaderCell>
            <CTableHeaderCell scope="col">제목</CTableHeaderCell>
            <CTableHeaderCell scope="col">담당자</CTableHeaderCell>
            <CTableHeaderCell scope="col">변경</CTableHeaderCell>
            <CTableHeaderCell scope="col"></CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="issue in issueList" :key="issue.pk" class="text-center">
            <CTableDataCell>
              <router-link
                :to="{
                  name: '(업무) - 보기',
                  params: { projId: issue.project.slug, issueId: issue.pk },
                }"
              >
                {{ issue.pk }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell v-if="!$route.params.projId">
              <router-link :to="{ name: '(개요)', params: { projId: issue.project.slug } }">
                {{ issue.project.name }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell>{{ issue.tracker.name }}</CTableDataCell>
            <CTableDataCell>{{ issue.status.name }}</CTableDataCell>
            <CTableDataCell>{{ issue.priority.name }}</CTableDataCell>
            <CTableDataCell class="text-left">
              <router-link
                :to="{
                  name: '(업무) - 보기',
                  params: { projId: issue.project.slug, issueId: issue.pk },
                }"
              >
                {{ issue.subject }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell class="text-center">
              <router-link
                v-if="issue.assigned_to"
                :to="{ name: '사용자 - 보기', params: { userId: issue.assigned_to?.pk } }"
              >
                {{ issue.assigned_to?.username }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell class="text-center">{{ timeFormat(issue.updated) }}</CTableDataCell>
            <CTableDataCell class="p-0">
              <span>
                <CDropdown color="secondary" variant="input-group" placement="bottom-end">
                  <CDropdownToggle
                    :caret="false"
                    color="light"
                    variant="ghost"
                    size="sm"
                    shape="rounded-pill"
                  >
                    <v-icon icon="mdi-dots-horizontal" class="pointer" color="grey-darken-1" />
                    <v-tooltip activator="parent" location="top">Actions</v-tooltip>
                  </CDropdownToggle>
                  <CDropdownMenu>
                    <CDropdownItem class="form-text">
                      <router-link to="">
                        <v-icon icon="mdi-pencil" color="amber" size="sm" />
                        편집
                      </router-link>
                    </CDropdownItem>
                    <!--                    <CDropdownItem class="form-text">-->
                    <!--                      <router-link to=""> 상태 </router-link>-->
                    <!--                    </CDropdownItem>-->
                    <!--                    <CDropdownItem class="form-text">-->
                    <!--                      <router-link to=""> 유형 </router-link>-->
                    <!--                    </CDropdownItem>-->
                    <!--                    <CDropdownItem class="form-text">-->
                    <!--                      <router-link to=""> 우선순위 </router-link>-->
                    <!--                    </CDropdownItem>-->
                    <!--                    <CDropdownItem class="form-text">-->
                    <!--                      <router-link to=""> 담당자 </router-link>-->
                    <!--                    </CDropdownItem>-->
                    <!--                    <CDropdownItem class="form-text">-->
                    <!--                      <router-link to=""> 진척도 </router-link>-->
                    <!--                    </CDropdownItem>-->
                    <!--                    <CDropdownItem class="form-text">-->
                    <!--                      <router-link to=""> 업무 관람자 </router-link>-->
                    <!--                    </CDropdownItem>-->
                    <CDropdownItem class="form-text">
                      <router-link to="">
                        <v-icon icon="mdi-star" color="secondary" size="sm" />
                        지켜보기
                      </router-link>
                    </CDropdownItem>
                    <CDropdownItem
                      class="form-text"
                      @click="
                        $router.push({
                          name: $route.params.projId ? '(소요시간) - 추가' : '소요시간 - 추가',
                          query: { issue_id: issue.pk },
                        })
                      "
                    >
                      <router-link to="">
                        <v-icon icon="mdi-calendar-clock" color="secondary" size="sm" />
                        작업시간 기록
                      </router-link>
                    </CDropdownItem>
                    <CDropdownItem class="form-text">
                      <router-link to="">
                        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
                        하위 업무 추가
                      </router-link>
                    </CDropdownItem>
                    <!--                    <CDropdownItem class="form-text">-->
                    <!--                      <router-link to="">-->
                    <!--                        <v-icon icon="mdi-link-edit" color="secondary" size="sm" />-->
                    <!--                        링크복사-->
                    <!--                      </router-link>-->
                    <!--                    </CDropdownItem>-->
                    <!--                    <CDropdownItem class="form-text">-->
                    <!--                      <router-link to="">-->
                    <!--                        <v-icon icon="mdi-content-copy" color="secondary" size="sm" />-->
                    <!--                        복사-->
                    <!--                      </router-link>-->
                    <!--                    </CDropdownItem>-->
                    <CDropdownItem class="form-text">
                      <router-link to="">
                        <v-icon icon="mdi-trash-can-outline" color="secondary" size="sm" />
                        삭제
                      </router-link>
                    </CDropdownItem>
                  </CDropdownMenu>
                </CDropdown>
              </span>
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
  </CRow>
</template>
