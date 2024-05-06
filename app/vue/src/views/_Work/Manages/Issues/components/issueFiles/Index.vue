<script lang="ts" setup>
import { onBeforeMount, type PropType, ref } from 'vue'
import type { IssueFile } from '@/store/types/work'
import { cutString, humanizeFileSize, timeFormat } from '@/utils/baseMixins'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  issueFiles: { type: Array as PropType<IssueFile[]>, default: () => [] },
})

const emit = defineEmits(['issue-file-control'])

const RefDelFile = ref()

// file 관련 코드
const editFile = ref(false)
const editNewFiles = ref<string | Blob[]>([])
const editDesc = ref<string[]>([])

const editFileSubmit = (pk: number, desc: string) => {
  const form = new FormData()
  form.append('edit_file', JSON.stringify(pk))
  form.append('edit_file_desc', desc)
  emit('issue-file-control', form)
  editFile.value = false
}

const delFile = ref<number | null>(null)
const delFileConfirm = (pk: number) => {
  delFile.value = pk
  RefDelFile.value.callModal()
}
const delFileSubmit = () => {
  const form = new FormData()
  form.append('del_file', JSON.stringify(delFile.value))
  emit('issue-file-control', form)
  delFile.value = null
  RefDelFile.value.close()
}

onBeforeMount(async () => {
  if (props.issueFiles) props.issueFiles.forEach(file => editDesc.value.push(file.description))
})
</script>

<template>
  <CRow class="mb-3">
    <CCol>
      <CRow class="mb-2">
        <CCol class="title">파일</CCol>
      </CRow>
      <CRow v-for="(file, i) in issueFiles" :key="file.pk">
        <CCol class="col-10">
          <v-icon icon="mdi-paperclip" size="sm" color="grey" class="mr-2" />
          <span>
            <a :href="file.file" target="_blank"> {{ cutString(file.file_name, 25) }} </a>
            <v-tooltip activator="parent" location="top">{{ file.file_name }}</v-tooltip>
          </span>
          <span class="file-desc1 mr-1"> ({{ humanizeFileSize(file.file_size) }}) </span>
          <span class="mr-2">
            <a :href="file.file" target="_blank">
              <v-icon icon="mdi-download-box" size="16" color="secondary" />
              <v-tooltip activator="parent" location="top">다운로드</v-tooltip>
            </a>
          </span>
          <span v-if="file.description" class="mr-2">{{ file.description }}</span>
          <span class="file-desc2 mr-1"> {{ file.user.username }}, </span>
          <span class="file-desc2 mr-2">{{ timeFormat(file.created) }}</span>
          <span>
            <router-link to="">
              <v-icon
                icon="mdi-trash-can-outline"
                size="16"
                color="secondary"
                class="mr-2"
                @click="delFileConfirm(file.pk)"
              />
              <v-tooltip activator="parent" location="top">삭제</v-tooltip>
            </router-link>
          </span>
        </CCol>

        <CCol v-if="i === 0" class="text-right form-text col-2">
          <span class="mr-2">
            <router-link to="">
              <v-icon icon="mdi-pencil" color="amber" size="18" @click="editFile = !editFile" />
            </router-link>
            <v-tooltip activator="parent" location="top">첨부파일 편집</v-tooltip>
          </span>

          <span v-if="issueFiles.length > 1" class="mr-2">
            <router-link to="">
              <v-icon icon="mdi-download-box" color="secondary" size="18" />
            </router-link>
            <v-tooltip activator="parent" location="top">전체 다운로드</v-tooltip>
          </span>
        </CCol>

        <template v-if="editFile">
          <CCol class="col-5">
            <CInputGroup size="sm">
              <CFormInput
                :id="`issue-file-${file.pk}`"
                type="file"
                placeholder="파일명"
                :disabled="!file.edit"
              />
              <CInputGroupText>
                <CFormCheck
                  :id="`change-file-${file.pk}`"
                  label="변경"
                  @click="file.edit = !file.edit"
                  class="my-0 py-0"
                />
              </CInputGroupText>
            </CInputGroup>
          </CCol>

          <CCol class="col-6">
            <CInputGroup>
              <CFormInput
                v-model="editDesc[i]"
                placeholder="부가적인 설명"
                @keydown.enter="editFileSubmit(file.pk, editDesc[i])"
              />
              <CInputGroupText
                v-if="editNewFiles[i] || file.description !== editDesc[i]"
                :id="`file-desc-${file.pk}`"
                @click="editFileSubmit(file.pk, editDesc[i])"
              >
                업데이트
              </CInputGroupText>
            </CInputGroup>
          </CCol>
        </template>
      </CRow>
    </CCol>
  </CRow>

  <v-divider />

  <ConfirmModal ref="RefDelFile">
    <template #default>이 파일 삭제를 계속 진행하시겠습니까?</template>
    <template #footer>
      <CButton color="warning" @click="delFileSubmit">삭제</CButton>
    </template>
  </ConfirmModal>
</template>

<style lang="scss" scoped>
.title {
  font-weight: bold;
}

.file-desc1 {
  font-size: 0.9em;
  color: #777;
}

.file-desc2 {
  font-size: 0.85em;
  color: #888;
}
</style>
