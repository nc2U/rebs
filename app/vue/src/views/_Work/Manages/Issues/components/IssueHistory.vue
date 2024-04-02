<script setup lang="ts">
import { type PropType, ref } from 'vue'
import type { IssueComment, IssueLogEntry, TimeEntry } from '@/store/types/work'
import { elapsedTime } from '@/utils/baseMixins'
import { VueMarkdownIt } from '@f3ve/vue-markdown-it'

defineProps({
  issueLogList: { type: Array as PropType<IssueLogEntry[]>, default: () => [] },
  issueCommentList: { type: Array as PropType<IssueComment[]>, default: () => [] },
  timeEntryList: { type: Array as PropType<TimeEntry[]>, default: () => [] },
})

const tabPaneActiveKey = ref(1)

const getHistory = (h: string) => h.split('|').filter(str => str.trim() !== '')

const copyLink = (path: string, hash: string) => {
  // 가상의 textarea 엘리먼트를 생성하고 텍스트를 할당.
  const textarea = document.createElement('textarea')
  textarea.value = window.location.host + '/#' + path + hash
  document.body.appendChild(textarea) // textarea를 DOM에 추가합니다.
  textarea.select() // textarea의 텍스트를 선택합니다.
  document.execCommand('copy') // 복사 명령을 실행합니다.
  document.body.removeChild(textarea) // textarea를 삭제합니다.
}
</script>

<template>
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
    <CNavItem v-if="issueCommentList.length">
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
    <CNavItem v-if="timeEntryList.length">
      <CNavLink
        href="javascript:void(0);"
        :active="tabPaneActiveKey === 4"
        @click="
          () => {
            tabPaneActiveKey = 4
          }
        "
      >
        작업시간
      </CNavLink>
    </CNavItem>
  </CNav>

  <CCard
    v-if="issueLogList.length"
    class="border-top-0 p-2"
    :style="{ '--cui-card-border-radius': 0 }"
  >
    <CCardBody>
      <CTabContent>
        <CTabPane role="tabpanel" aria-labelledby="home-tab" :visible="tabPaneActiveKey === 1">
          <div v-for="log in issueLogList" :key="log.pk">
            <CRow
              :id="`note-${log.pk}`"
              :class="{ 'bg-blue-lighten-5': $route.hash == `#note-${log.pk}` }"
            >
              <!--              {{ $route.fullPath }}-->
              <CCol v-if="log.user">
                <router-link :to="{ name: '사용자 - 보기', params: { userId: log.user.pk } }">
                  {{ log.user.username }}
                </router-link>
                이(가)
                <router-link
                  :to="{
                    name: '(작업내역)',
                    params: { projId: log.issue.project.slug },
                    query: { from: log.timestamp.substring(0, 10) },
                  }"
                >
                  {{ elapsedTime(log.timestamp) }}
                </router-link>
                에 변경
              </CCol>
              <CCol class="text-right">
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
                      <CDropdownItem
                        class="form-text"
                        @click="copyLink($route.path, `#note-${log.pk}`)"
                      >
                        <router-link to="">
                          <v-icon icon="mdi-pencil" color="amber" size="sm" />
                          링크 복사
                        </router-link>
                      </CDropdownItem>
                    </CDropdownMenu>
                  </CDropdown>
                </span>
                <router-link :to="{ hash: '#note-' + log.pk }">#{{ log.pk }}</router-link>
              </CCol>
            </CRow>
            <v-divider class="mt-0 mb-2" />
            <div class="history pl-4 mb-2">
              <ul>
                <li v-for="(src, i) in getHistory(log.details)" :key="i">
                  <VueMarkdownIt :source="src" />
                  <span v-if="log.diff && src.includes('**설명**')">
                    <router-link to="">
                      (변경 내용)
                      <v-tooltip activator="parent" location="start">
                        <VueMarkdownIt :source="log.diff" />
                      </v-tooltip>
                    </router-link>
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </CTabPane>

        <CTabPane role="tabpanel" aria-labelledby="profile-tab" :visible="tabPaneActiveKey === 2">
          <div v-for="comment in issueCommentList" :key="comment.pk">
            <CRow
              :id="`note-${comment.pk}`"
              :class="{ 'bg-blue-lighten-5': $route.hash == `#note-${comment.pk}` }"
            >
              <CCol v-if="comment.user">
                <router-link :to="{ name: '사용자 - 보기', params: { userId: comment.user.pk } }">
                  {{ comment.user.username }}
                </router-link>
                이(가)
                <router-link
                  :to="{
                    name: '(작업내역)',
                    params: { projId: comment.issue.project.slug },
                    query: { from: comment.created.substring(0, 10) },
                  }"
                >
                  {{ elapsedTime(comment.created) }}
                </router-link>
                에 변경
              </CCol>
              <CCol class="text-right">
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
                      <CDropdownItem
                        class="form-text"
                        @click="copyLink($route.path, `#note-${comment.pk}`)"
                      >
                        <router-link to="">
                          <v-icon icon="mdi-pencil" color="amber" size="sm" />
                          링크 복사
                        </router-link>
                      </CDropdownItem>
                      <CDropdownItem
                        class="form-text"
                        @click="copyLink($route.path, `#note-${comment.pk}`)"
                      >
                        <router-link to="">
                          <v-icon icon="mdi-trash-can" color="grey" size="sm" />
                          삭제
                        </router-link>
                      </CDropdownItem>
                    </CDropdownMenu>
                  </CDropdown>
                </span>
                <router-link :to="{ hash: '#note-' + comment.pk }">#{{ comment.pk }}</router-link>
              </CCol>
            </CRow>
            <v-divider class="mt-0 mb-2" />
            <div class="history pl-4 mb-2">
              <VueMarkdownIt :source="comment.content" class="markdown-body" />
            </div>
          </div>
        </CTabPane>

        <CTabPane role="tabpanel" aria-labelledby="contact-tab" :visible="tabPaneActiveKey === 3">
          <div v-for="log in issueLogList" :key="log.pk">
            <CRow
              :id="`note-${log.pk}`"
              :class="{ 'bg-blue-lighten-5': $route.hash == `#note-${log.pk}` }"
            >
              <CCol v-if="log.user">
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
              <CCol class="text-right">
                <router-link :to="{ hash: '#note-' + log.pk }">#{{ log.pk }}</router-link>
              </CCol>
            </CRow>
            <v-divider class="mt-0 mb-2" />
            <div class="history pl-4 mb-2">
              <ul>
                <li v-for="(src, i) in getHistory(log.details)" :key="i">
                  <VueMarkdownIt :source="src" />
                  <span v-if="log.diff && src.includes('**설명**')">
                    <router-link to="">
                      (변경 내용)
                      <v-tooltip activator="parent" location="start">
                        <VueMarkdownIt :source="log.diff" />
                      </v-tooltip>
                    </router-link>
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </CTabPane>

        <CTabPane role="tabpanel" aria-labelledby="profile-tab" :visible="tabPaneActiveKey === 4">
          <div v-for="time in timeEntryList" :key="time.pk">
            <CRow>
              <CCol v-if="time.user">
                <router-link :to="{ name: '사용자 - 보기', params: { userId: time.user.pk } }">
                  {{ time.user.username }}
                </router-link>
                이(가)
                <router-link
                  :to="{
                    name: '(작업내역)',
                    params: { projId: 'redmine' },
                    query: { from: time.created.substring(0, 10) },
                  }"
                >
                  {{ elapsedTime(time.created) }}
                </router-link>
                에 추가함
              </CCol>
              <CCol class="text-right pr-3">
                <span>
                  <v-icon
                    icon="mdi-pencil"
                    color="amber"
                    class="mr-2 pointer"
                    size="18"
                    @click="
                      $router.push({
                        name: '(소요시간) - 편집',
                        params: { projId: time.issue.project.slug, timeId: time.pk },
                      })
                    "
                  />
                  <v-tooltip activator="parent" location="top">편집</v-tooltip>
                </span>

                <span>
                  <v-icon icon="mdi-trash-can" color="grey" size="18" class="pointer" />
                  <v-tooltip activator="parent" location="top">삭제</v-tooltip>
                </span>
              </CCol>
            </CRow>
            <v-divider class="mt-0 mb-2" />
            <div class="history pl-4 mb-2">
              <ul>
                <li>작업시간 : {{ time.hours }} 시간</li>
              </ul>
            </div>
            <div class="mb-2">{{ time.comment }}</div>
          </div>
        </CTabPane>
      </CTabContent>
    </CCardBody>
  </CCard>
</template>

<style lang="scss" scoped>
.history {
  color: #7f7f7f;
}

.vue-md-it-wrapper blockquote {
  padding-left: 20px !important;
  border-left: 3px solid #ddd !important;
  font-style: italic;
}
</style>
