<script lang="ts" setup="">
import { ref, type PropType } from 'vue'
import type { Issue, LogEntry } from '@/store/types/work'
import { timeFormat, elapsedTime, dateFormat } from '@/utils/baseMixins'

defineProps({
  issue: { type: Object as PropType<Issue>, default: null },
  logEntryList: { type: Array as PropType<LogEntry[]>, default: () => [] },
})

const tabPaneActiveKey = ref(1)
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>
        <span>{{ issue?.tracker }} #{{ issue?.pk }}</span>
        <CBadge color="primary" variant="outline" class="ml-2">진행중</CBadge>
      </h5>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-pencil" color="amber" size="sm" />
        <router-link to="" class="ml-1">편집</router-link>
      </span>

      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-timer-edit-outline" color="grey" size="sm" />
        <router-link to="" class="ml-1">작업시간 기록</router-link>
      </span>

      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-star" color="amber" size="sm" />
        <router-link to="" class="ml-1">관심끄기</router-link>
      </span>

      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-content-copy" color="grey" size="sm" />
        <router-link to="" class="ml-1">복사</router-link>
      </span>

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
            <CDropdownItem>
              <router-link to="">
                <v-icon icon="mdi-link-plus" color="grey" size="sm" />
                링크 복사
              </router-link>
            </CDropdownItem>
            <CDropdownItem>
              <router-link to="">
                <v-icon icon="mdi-trash-can-outline" color="grey" size="sm" />
                업무 삭제
              </router-link>
            </CDropdownItem>
          </CDropdownMenu>
        </CDropdown>
      </span>
    </CCol>
  </CRow>

  <CCard color="yellow-lighten-5 mb-3">
    <CCardBody>
      <span class="sub-title">권한별 프로젝트 목록 보기</span>
      <p class="mt-1">
        <router-link to="">austin2 kho</router-link>
        이(가)
        <router-link to="">23분</router-link>
        전에 추가함.
        <router-link to="">22분</router-link>
        전에 수정됨.
      </p>

      <CRow>
        <CCol md="6">
          <CRow>
            <CCol class="title">상태 :</CCol>
            <CCol>{{ issue?.status }}</CCol>
          </CRow>
          <CRow>
            <CCol class="title">우선순위 :</CCol>
            <CCol>{{ issue?.priority }}</CCol>
          </CRow>
          <CRow>
            <CCol class="title">담당자 :</CCol>
            <CCol>
              <router-link
                :to="{ name: '사용자 - 보기', params: { userId: issue?.assigned_to?.pk ?? 0 } }"
              >
                {{ issue?.assigned_to?.username }}
              </router-link>
            </CCol>
          </CRow>
          <CRow>
            <CCol class="title"></CCol>
            <CCol></CCol>
          </CRow>
        </CCol>

        <CCol md="6">
          <CRow>
            <CCol class="title">시작일 :</CCol>
            <CCol>{{ issue?.start_date }}</CCol>
          </CRow>
          <CRow>
            <CCol class="title">완료일 :</CCol>
            <CCol>{{ issue?.due_date }}</CCol>
          </CRow>
          <CRow>
            <CCol class="title">진척도 :</CCol>
            <CCol>
              <div>
                <CProgress
                  color="success"
                  :value="20"
                  style="width: 110px; float: left; margin-top: 2px"
                  height="16"
                />
                <span class="ml-2 pt-0">{{ issue?.done_ratio }}%</span>
              </div>
            </CCol>
          </CRow>

          <CRow>
            <CCol class="title">추정시간:</CCol>
            <CCol>{{ issue?.estimated_hours ? issue.estimated_hours + ':00 시간' : '' }}</CCol>
          </CRow>
        </CCol>
      </CRow>

      <v-divider />

      <CRow class="mb-3">
        <CCol class="title">설명</CCol>
        <CCol class="text-right">
          <v-icon icon="mdi-comment-text-outline" size="sm" color="grey" class="mr-2" />
          <router-link to="">댓글달기</router-link>
        </CCol>
      </CRow>

      <CRow>
        <CCol>
          {{ issue?.description }}
        </CCol>
      </CRow>

      <v-divider />

      <CRow>
        <CCol class="title">하위 일감</CCol>
        <CCol class="text-right">
          <router-link to="">추가</router-link>
        </CCol>
      </CRow>

      <v-divider />

      <CRow>
        <CCol class="title">연결된 일감</CCol>
        <CCol class="text-right">
          <router-link to="">추가</router-link>
        </CCol>
      </CRow>
    </CCardBody>
  </CCard>

  <CNav variant="tabs">
    <CNavItem>
      <CNavLink
        href="javascript:void(0);"
        :active="tabPaneActiveKey === 1"
        @click="
          () => {
            tabPaneActiveKey = 1
          }
        "
      >
        이력
      </CNavLink>
    </CNavItem>
    <CNavItem v-if="true">
      <CNavLink
        href="javascript:void(0);"
        :active="tabPaneActiveKey === 2"
        @click="
          () => {
            tabPaneActiveKey = 2
          }
        "
      >
        댓글
      </CNavLink>
    </CNavItem>
    <CNavItem>
      <CNavLink
        href="javascript:void(0);"
        :active="tabPaneActiveKey === 3"
        @click="
          () => {
            tabPaneActiveKey = 3
          }
        "
      >
        항목 변경이력
      </CNavLink>
    </CNavItem>
  </CNav>

  <CCard class="border-top-0 p-2" :style="{ '--cui-card-border-radius': 0 }">
    <CCardBody>
      <CTabContent>
        <CTabPane role="tabpanel" aria-labelledby="home-tab" :visible="tabPaneActiveKey === 1">
          <div v-for="log in logEntryList" :key="log.pk">
            <CRow>
              <CCol>
                <router-link :to="{ name: '사용자 - 보기', params: { userId: log.user.pk } }">
                  {{ log.user.username }}
                </router-link>
                이(가)
                <router-link
                  :to="{
                    name: '(작업내역)',
                    params: { projId: 'redmine' },
                    query: { from: log.timestamp.substring(0, 10) },
                  }"
                >
                  {{ elapsedTime(log.timestamp) }}
                </router-link>
                에 변경
              </CCol>
              <CCol class="text-right">#{{ log.pk }}</CCol>
            </CRow>
            <v-divider class="mt-0" />
            <ul class="pl-4">
              <li>{{ log.details }}</li>
            </ul>
          </div>
        </CTabPane>
        <CTabPane role="tabpanel" aria-labelledby="profile-tab" :visible="tabPaneActiveKey === 2">
          Food truck fixie locavore, accusamus mcsweeney's marfa nulla single-origin coffee squid.
          Exercitation +1 labore velit, blog sartorial PBR leggings next level wes anderson artisan
          four loko farm-to-table craft beer twee. Qui photo booth letterpress, commodo enim craft
          beer mlkshk aliquip jean shorts ullamco ad vinyl cillum PBR. Homo nostrud organic,
          assumenda labore aesthetic magna delectus mollit. Keytar helvetica VHS salvia yr, vero
          magna velit sapiente labore stumptown. Vegan fanny pack odio cillum wes anderson 8-bit,
          sustainable jean shorts beard ut DIY ethical culpa terry richardson biodiesel. Art party
          scenester stumptown, tumblr butcher vero sint qui sapiente accusamus tattooed echo park.
        </CTabPane>
        <CTabPane role="tabpanel" aria-labelledby="contact-tab" :visible="tabPaneActiveKey === 3">
          <ul v-for="log in logEntryList" :key="log.pk">
            <li>{{ log.details }}</li>
          </ul>
        </CTabPane>
      </CTabContent>
    </CCardBody>
  </CCard>
</template>

<style lang="scss" scoped>
.title {
  font-weight: bold;
}

.sub-title {
  font-size: 1.1em;
  font-weight: bold;
  color: #0f192a;
}
</style>
