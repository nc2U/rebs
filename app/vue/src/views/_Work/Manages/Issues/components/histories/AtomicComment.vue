<script lang="ts" setup>
import { type PropType, ref } from 'vue'
import type { IssueLogEntry } from '@/store/types/work'
import { elapsedTime, timeFormat } from '@/utils/baseMixins'
import { VueMarkdownIt } from '@f3ve/vue-markdown-it'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

defineProps({ log: { type: Object as PropType<IssueLogEntry>, required: true } })

const emit = defineEmits(['del-submit'])

const RefDelConfirm = ref()
const delPk = ref<null | number>(null)

const toReply = (pk?: number | null) => alert(`reply - ${pk}`)
const toEdit = (pk?: number | null) => alert(`edit - ${pk}`)

const copyLink = (path: string, hash: string) => {
  // 가상의 textarea 엘리먼트를 생성하고 텍스트를 할당.
  const textarea = document.createElement('textarea')
  textarea.value = window.location.host + '/#' + path + hash
  document.body.appendChild(textarea) // textarea를 DOM에 추가합니다.
  textarea.select() // textarea의 텍스트를 선택합니다.
  document.execCommand('copy') // 복사 명령을 실행합니다.
  document.body.removeChild(textarea) // textarea를 삭제합니다.
}

const delConfirm = (pk: number) => {
  delPk.value = pk
  RefDelConfirm.value.callModal('삭제 확인', '계속 진행하시겠습니까?', '', 'warning')
}

const delSubmit = () => {
  emit('del-submit', delPk.value)
  delPk.value = null
  RefDelConfirm.value.close()
}
</script>

<template>
  <CRow>
    <CCol>
      <CRow
        :id="`note-${log.pk}`"
        :class="{ 'bg-blue-lighten-5': $route.hash == `#note-${log.log_id}` }"
      >
        <CCol v-if="log.user" class="pt-1">
          <router-link :to="{ name: '사용자 - 보기', params: { userId: log.user.pk } }">
            {{ log.user.username }}
          </router-link>
          이(가)
          <span>
            <router-link
              :to="{
                name: '(작업내역)',
                params: { projId: 'redmine' },
                query: { from: log.timestamp.substring(0, 10) },
              }"
            >
              {{ elapsedTime(log.timestamp) }}
            </router-link>
            <v-tooltip activator="parent" location="top">{{ timeFormat(log.timestamp) }}</v-tooltip>
          </span>
          에 변경
        </CCol>
        <CCol class="text-right">
          <span>
            <v-icon
              icon="mdi-comment-processing-outline"
              color="info"
              size="16"
              class="mr-2 pointer"
              @click="toReply(log.comment?.pk)"
            />
            <v-tooltip activator="parent" location="top">댓글달기</v-tooltip>
          </span>
          <span>
            <v-icon
              icon="mdi-pencil"
              color="amber"
              size="16"
              class="mr-1 pointer"
              @click="toEdit(log.comment?.pk)"
            />
            <v-tooltip activator="parent" location="top">편집</v-tooltip>
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
                <CDropdownItem
                  class="form-text"
                  @click="copyLink($route.path, `#note-${log.log_id}`)"
                >
                  <router-link to="">
                    <v-icon icon="mdi-pencil" color="amber" size="sm" />
                    링크 복사
                  </router-link>
                </CDropdownItem>
                <CDropdownItem class="form-text" @click="delConfirm(log.comment?.pk as number)">
                  <router-link to="">
                    <v-icon icon="mdi-trash-can" color="grey" size="sm" />
                    삭제
                  </router-link>
                </CDropdownItem>
              </CDropdownMenu>
            </CDropdown>
          </span>

          <router-link :to="{ hash: '#note-' + log.log_id }">#{{ log.log_id }}</router-link>
        </CCol>
      </CRow>
      <v-divider class="mt-0 mb-2" />
      <div class="history pl-4">
        <VueMarkdownIt :source="log.comment?.content + '\n' ?? '\n'" />
      </div>

      <ConfirmModal ref="RefDelConfirm">
        <template #footer>
          <CButton color="danger" @click="delSubmit">확인</CButton>
        </template>
      </ConfirmModal>
    </CCol>
  </CRow>
</template>
