<script setup lang="ts">
import { type PropType, ref } from 'vue'
import type { LogEntry } from '@/store/types/work'
import { elapsedTime } from '@/utils/baseMixins'
import { VueMarkdownIt } from '@f3ve/vue-markdown-it'

defineProps({
  logEntryList: { type: Array as PropType<LogEntry[]>, default: () => [] },
})

const tabPaneActiveKey = ref(1)

const getHistory = (h: string) => h.split('|').filter(str => str.trim() !== '')
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

  <CCard
    v-if="logEntryList.length"
    class="border-top-0 p-2"
    :style="{ '--cui-card-border-radius': 0 }"
  >
    <CCardBody>
      <CTabContent>
        <CTabPane role="tabpanel" aria-labelledby="home-tab" :visible="tabPaneActiveKey === 1">
          <div v-for="log in logEntryList" :key="log.pk">
            <CRow>
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
              <CCol class="text-right">#{{ log.pk }}</CCol>
            </CRow>
            <v-divider class="mt-0 mb-2" />
            <div class="history pl-4 mb-2">
              <ul>
                <li v-for="(src, i) in getHistory(log.details)" :key="i">
                  <VueMarkdownIt :source="src" />
                  <span v-if="log.diff">
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
          <span class="history">
            Food truck fixie locavore, accusamus mcsweeney's marfa nulla single-origin coffee squid.
            Exercitation +1 labore velit, blog sartorial PBR leggings next level wes anderson
            artisan four loko farm-to-table craft beer twee. Qui photo booth letterpress, commodo
            enim craft beer mlkshk aliquip jean shorts ullamco ad vinyl cillum PBR. Homo nostrud
            organic, assumenda labore aesthetic magna delectus mollit. Keytar helvetica VHS salvia
            yr, vero magna velit sapiente labore stumptown. Vegan fanny pack odio cillum wes
            anderson 8-bit, sustainable jean shorts beard ut DIY ethical culpa terry richardson
            biodiesel. Art party scenester stumptown, tumblr butcher vero sint qui sapiente
            accusamus tattooed echo park.
          </span>
        </CTabPane>

        <CTabPane role="tabpanel" aria-labelledby="contact-tab" :visible="tabPaneActiveKey === 3">
          <div v-for="log in logEntryList" :key="log.pk">
            <CRow>
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
              <CCol class="text-right">#{{ log.pk }}</CCol>
            </CRow>
            <v-divider class="mt-0 mb-2" />
            <div class="history pl-4 mb-2">
              <ul>
                <li v-for="(src, i) in getHistory(log.details)" :key="i">
                  <VueMarkdownIt :source="src" />
                  <span v-if="log.diff">
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
      </CTabContent>
    </CCardBody>
  </CCard>
</template>

<style lang="scss" scoped>
.history {
  color: #7f7f7f;

  ul {
    margin: 0 !important;
    padding: 0 !important;
  }
}

.vue-md-wrapper ul {
  margin: 0;
  padding: 0;
}
</style>
