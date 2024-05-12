<script lang="ts" setup="">
import { ref } from 'vue'
import { cutString, humanizeFileSize } from '@/utils/baseMixins'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

defineProps({
  isDark: { type: Boolean, default: false },
  status: { type: String, default: '' },
  contractFiles: { type: Array, default: () => [] },
})

const emit = defineEmits(['cont-file-control'])

const RefDelFile = ref()

const newFiles = ref<{ file: File }[]>([])

const editMode = ref(false)
const editFiles = ref<{ file: File }[]>([])

const loadFile = (data: Event, mode = 'new') => {
  const el = data.target as HTMLInputElement
  if (el.files && el.files[0]) {
    if (el.id === 'scan-new-file') newFiles.value.push({ file: el.files[0] })
    else editFiles.value.push({ file: el.files[0] })
  }
}

const removeFile = id => {
  const file_form = document.getElementById(id) as HTMLInputElement
  file_form.value = ''
  if (id === 'scan-new-file') newFiles.value = []
  else editFiles.value = []
}

const delFile = ref<number | null>(null)
const delFileConfirm = (pk: number) => {
  delFile.value = pk
  RefDelFile.value.callModal()
}

const delFileSubmit = () => {
  // const form = new FormData()
  // form.append('del_file', JSON.stringify(delFile.value))
  emit('cont-file-control', { del_file: delFile.value })
  delFile.value = null
  RefDelFile.value.close()
}
</script>

<template>
  <CRow class="my-3 py-2" :class="{ 'bg-light': !isDark }">
    <CFormLabel class="col-sm-2 col-lg-1 col-form-label"> 계약서 파일</CFormLabel>
    <CCol sm="10" class="mb-sm-3 mb-lg-0">
      <template v-if="!!contractFiles.length">
        <CRow v-for="file in contractFiles" :key="file.pk" class="mb-2" style="padding-top: 6px">
          <CCol>
            <v-icon icon="mdi-paperclip" size="sm" color="grey" class="mr-2" />
            <span>
              <a :href="file.file" target="_blank">
                {{ cutString(file.file_name, 50) }}
              </a>
            </span>
            <span class="file-desc1 form-text mr-1">
              ({{ humanizeFileSize(file.file_size) }})
            </span>
          </CCol>
          <CCol class="text-right">
            <v-icon
              icon="mdi-pencil"
              color="success"
              size="18"
              class="pointer"
              @click="editMode = !editMode"
            />
            <v-icon
              icon="mdi-trash-can-outline"
              color="grey"
              size="18"
              class="pointer ml-2"
              @click="delFileConfirm(file.pk)"
            />
          </CCol>
        </CRow>
      </template>
      <CInputGroup v-else>
        <CFormInput id="scan-new-file" type="file" @change="loadFile" :disabled="!status" />
        <CInputGroupText v-if="!!newFiles.length">
          <v-icon
            icon="mdi-trash-can-outline"
            color="grey"
            size="16"
            @click="removeFile('scan-new-file')"
          />
        </CInputGroupText>
      </CInputGroup>

      <CInputGroup v-if="editMode">
        <CFormInput id="scan-edit-file" type="file" @change="loadFile" :disabled="!status" />
        <CInputGroupText v-if="!!editFiles.length">
          <v-icon
            icon="mdi-trash-can-outline"
            color="grey"
            size="16"
            @click="removeFile('scan-edit-file')"
          />
        </CInputGroupText>
      </CInputGroup>
    </CCol>
  </CRow>

  <ConfirmModal ref="RefDelFile">
    <template #default>이 파일 삭제를 계속 진행하시겠습니까?</template>
    <template #footer>
      <CButton color="warning" @click="delFileSubmit">삭제</CButton>
    </template>
  </ConfirmModal>
</template>
