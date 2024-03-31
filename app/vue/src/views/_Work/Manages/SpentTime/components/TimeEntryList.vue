<script lang="ts" setup>
import { type PropType } from 'vue'
import type { TimeEntry } from '@/store/types/work'
import { dateFormat, numberToHour } from '@/utils/baseMixins'
import NoData from '@/views/_Work/components/NoData.vue'
import SearchList from '@/views/_Work/components/SearchList.vue'
import HeaderTab from '@/views/_Work/Manages/SpentTime/components/HeaderTab.vue'

defineProps({
  timeEntryList: { type: Array as PropType<TimeEntry[]>, default: () => [] },
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>소요시간</h5>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2 form-text">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link
          :to="{ name: $route.params.projId ? '(소요시간) - 추가' : '소요시간 - 추가' }"
          class="ml-1"
        >
          작업시간 기록
        </router-link>
      </span>
    </CCol>
  </CRow>

  <SearchList />

  <HeaderTab />

  <NoData v-if="!timeEntryList.length" />

  <CRow v-else>
    <CCol col="12">
      <CRow class="mb-1 text-right pr-2">
        <CCol class="">
          <span>소요시간 합계 : </span>
          <span class="bold">{{ numberToHour(timeEntryList[0].total_hours ?? 0) }}</span>
        </CCol>
      </CRow>
      <v-divider class="my-0" />
      <CTable striped hover small responsive>
        <colgroup>
          <col v-if="!$route.params.projId" style="width: 18%" />
          <col style="width: 10%" />
          <col style="width: 10%" />
          <col style="width: 8%" />
          <col style="width: 20%" />
          <col style="width: 20%" />
          <col style="width: 9%" />
          <col style="width: 5%" />
        </colgroup>
        <CTableHead>
          <CTableRow class="text-center">
            <CTableHeaderCell v-if="!$route.params.projId" scope="col">프로젝트</CTableHeaderCell>
            <CTableHeaderCell scope="col">작업일자</CTableHeaderCell>
            <CTableHeaderCell scope="col">사용자</CTableHeaderCell>
            <CTableHeaderCell scope="col">작업종류</CTableHeaderCell>
            <CTableHeaderCell scope="col">업무</CTableHeaderCell>
            <CTableHeaderCell scope="col">설명</CTableHeaderCell>
            <CTableHeaderCell scope="col">시간</CTableHeaderCell>
            <CTableHeaderCell scope="col"></CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="time in timeEntryList" :key="time.pk" class="text-center">
            <CTableDataCell v-if="!$route.params.projId">
              <router-link to="">{{ time.issue.project }}</router-link>
            </CTableDataCell>
            <CTableDataCell class="text-center">
              {{ dateFormat(time.spent_on, '/') }}
            </CTableDataCell>
            <CTableDataCell>
              <router-link :to="{ name: '사용자 - 보기', params: { userId: time.user.pk } }">
                {{ time.user.username }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell>{{ time.activity }}</CTableDataCell>
            <CTableDataCell class="text-left">
              <router-link to=""> {{ time.issue.tracker }} #{{ time.issue.pk }}</router-link>
              : {{ time.issue.subject }}
            </CTableDataCell>
            <CTableDataCell class="text-left">
              {{ time.comment }}
            </CTableDataCell>
            <CTableDataCell>
              <span class="strong">{{ numberToHour(time.hours) }}</span>
            </CTableDataCell>
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
                      <router-link to=""> 작업종류 </router-link>
                    </CDropdownItem>
                    <CDropdownItem class="form-text">
                      <router-link to="">
                        <v-icon icon="mdi-pencil" color="amber" size="sm" />
                        편집
                      </router-link>
                    </CDropdownItem>
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
