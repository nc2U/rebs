<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount, onUpdated, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useDocument } from '@/store/pinia/document'
import { Post, Attatches } from '@/store/types/document'
import { write_company_docs } from '@/utils/pageAuth'
import { dateFormat } from '@/utils/baseMixins'
import { AlertSecondary } from '@/utils/cssMixins'
import ToastEditor from '@/components/ToastEditor/index.vue'
import FileUpload from '@/components/FileUpload.vue'
import DatePicker from '@/components/DatePicker/index.vue'
import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  categoryList: { type: Object, required: true },
  getSuitCase: { type: Object, required: true },
  post: { type: Object, default: null },
})

const emit = defineEmits(['on-submit', 'close'])

const delModal = ref()
const alertModal = ref()
const confirmModal = ref()

const attach = ref(true)
const validated = ref(false)
const form = reactive<Post & Attatches>({
  pk: null,
  company: null,
  project: null,
  board: 3,
  is_notice: false,
  category: null,
  lawsuit: null,
  title: '',
  execution_date: null,
  content: '',
  is_hide_comment: false,
  hit: 0,
  blame: 0,
  ip: null,
  device: '',
  secret: false,
  password: '',
  oldLinks: [],
  oldFiles: [],
  newLinks: [],
  newFiles: [],
})

watch(form, val => {
  if (val.execution_date) form.execution_date = dateFormat(val.execution_date)
})

const formsCheck = computed(() => {
  if (props.post) {
    const a = form.is_notice === props.post.is_notice
    const b = form.category === props.post.category
    const c = form.lawsuit === props.post.lawsuit
    const d = form.title === props.post.title
    const e = form.execution_date === props.post.execution_date
    const f = form.content === props.post.content

    return a && b && c && d && e && f && attach.value
  } else return false
})

const documentStore = useDocument()
const getSuitCase = computed(() => documentStore.getSuitCase)

const newLinkNum = ref(1)
const newLinkRange = computed(() => {
  let array = []
  for (let i = 0; i < newLinkNum.value; ++i) array.push(i)
  return array
})

const newFileNum = ref(1)
const newFileRange = computed(() => {
  let array = []
  for (let i = 0; i < newFileNum.value; ++i) array.push(i)
  return array
})

const sortName = computed(() =>
  props.post && props.post.project ? props.post.proj_name : '본사',
)

const route = useRoute()
const btnClass = computed(() => (route.params.postId ? 'success' : 'primary'))

const ctlLinkNum = (n: number) => {
  if (n + 1 >= newLinkNum.value) newLinkNum.value = newLinkNum.value + 1
  else newLinkNum.value = newLinkNum.value - 1
}

const ctlFileNum = (n: number) => {
  if (n + 1 >= newFileNum.value) newFileNum.value = newFileNum.value + 1
  else newFileNum.value = newFileNum.value - 1
}

const enableStore = (event: Event) => {
  const el = event.target as HTMLInputElement
  attach.value = !el.value
}

const onSubmit = (event: Event) => {
  if (write_company_docs) {
    const el = event.currentTarget as HTMLSelectElement
    if (!el.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else confirmModal.value.callModal()
  } else alertModal.value.callModal()
}

const modalAction = () => {
  emit('on-submit', { ...form })
  validated.value = false
  confirmModal.value.close()
}

const devideUri = (uri: string) => {
  const devidedUri = decodeURI(uri).split('media/')
  return [devidedUri[0] + 'media/', devidedUri[1]]
}

const dataSetup = () => {
  if (props.post) {
    form.pk = props.post.pk
    form.company = props.post.company
    form.project = props.post.project
    form.board = props.post.board
    form.is_notice = props.post.is_notice
    form.category = props.post.category
    form.lawsuit = props.post.lawsuit
    form.title = props.post.title
    form.execution_date = props.post.execution_date
    form.content = props.post.content
    form.is_hide_comment = props.post.is_hide_comment
    form.hit = props.post.hit
    form.blame = props.post.blame
    form.blame = props.post.blame
    form.device = props.post.device
    form.secret = props.post.secret
    form.password = props.post.password
    if (props.post.links) form.oldLinks = props.post.links
    if (props.post.files) {
      form.oldFiles = props.post.files.map((file: any) => ({
        pk: file.pk,
        file: file.file,
        newFile: '',
        hit: file.hit,
      }))
    }
  }
}

onUpdated(() => dataSetup())
onBeforeMount(() => dataSetup())
</script>

<template>
  <CRow class="mt-5">
    <CCol>
      <h5>
        {{ sortName }}
        <v-icon icon="mdi-chevron-double-right" size="xs" />
        소송 문서
      </h5>
    </CCol>
  </CRow>

  <hr />

  <CForm
    enctype="multipart/form-data"
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="mb-3">
      <CFormLabel for="title" class="col-md-2 col-form-label">제목</CFormLabel>
      <CCol md="9">
        <CFormInput
          id="title"
          v-model="form.title"
          required
          placeholder="게시물 제목"
        />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="inputPassword" class="col-sm-2 col-form-label">
        사건번호 (사건번호 등록)
      </CFormLabel>
      <CCol md="3">
        <Multiselect
          v-model="form.lawsuit"
          :options="getSuitCase"
          placeholder="사건번호 선택"
          autocomplete="label"
          :classes="{ search: 'form-control multiselect-search' }"
          :attrs="form.lawsuit ? {} : { required: true }"
          :add-option-on="['enter' | 'tab']"
          searchable
        />
      </CCol>

      <CFormLabel for="category" class="col-md-2 col-lg-1 col-form-label">
        카테고리
      </CFormLabel>
      <CCol md="2">
        <CFormSelect id="category" v-model="form.category" required>
          <option value="">카테고리 선택</option>
          <option v-for="cate in categoryList" :key="cate.pk" :value="cate.pk">
            {{ cate.name }}
          </option>
        </CFormSelect>
      </CCol>

      <CFormLabel for="inputPassword" class="col-md-2 col-lg-1 col-form-label">
        문서 발행일자
      </CFormLabel>
      <CCol md="2">
        <DatePicker
          v-model="form.execution_date"
          placeholder="문서 발행일자"
          required
        />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="title" class="col-md-2 col-form-label">내용</CFormLabel>
      <CCol md="10">
        <ToastEditor v-model="form.content" placeholder="본문 내용" />
      </CCol>
    </CRow>

    <CRow>
      <CFormLabel for="title" class="col-md-2 col-form-label">링크</CFormLabel>
      <CCol md="10" lg="8" xl="6">
        <CRow v-if="post && form.oldLinks.length">
          <CAlert :color="AlertSecondary">
            <CCol>
              <CInputGroup
                v-for="(link, i) in form.oldLinks"
                :key="link.pk"
                class="mb-2"
              >
                <CFormInput
                  :id="`post-link-${link.pk}`"
                  v-model="form.oldLinks[i].link"
                  size="sm"
                  placeholder="파일 링크"
                  @input="enableStore"
                />
                <CInputGroupText id="basic-addon1" class="py-0">
                  <CFormCheck
                    :id="`del-link-${link.pk}`"
                    v-model="form.oldLinks[i].del"
                    :value="false"
                    label="삭제"
                    @input="enableStore"
                  />
                </CInputGroupText>
              </CInputGroup>
            </CCol>
          </CAlert>
        </CRow>

        <CRow class="mb-2">
          <CCol>
            <CInputGroup
              v-for="lNum in newLinkRange"
              :key="`ln-${lNum}`"
              class="mb-2"
            >
              <CFormInput
                :id="`link-${lNum}`"
                v-model="form.newLinks[lNum]"
                placeholder="파일 링크"
                @input="enableStore"
              />
              <CInputGroupText id="basic-addon1" @click="ctlLinkNum(lNum)">
                <v-icon
                  :icon="`mdi-${
                    lNum + 1 < newLinkNum ? 'minus' : 'plus'
                  }-thick`"
                  :color="lNum + 1 < newLinkNum ? 'error' : 'primary'"
                />
              </CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="title" class="col-md-2 col-form-label">파일</CFormLabel>
      <CCol md="10" lg="8" xl="6">
        <CRow v-if="post && form.oldFiles.length">
          <CAlert :color="AlertSecondary">
            <small>{{ devideUri(form.oldFiles[0].file)[0] }}</small>
            <CCol
              v-for="(file, i) in form.oldFiles"
              :key="file.pk"
              xs="12"
              color="primary"
            >
              <small>
                현재 :
                <a :href="file.file" target="_blank">
                  {{ devideUri(file.file)[1] }}
                </a>
                <CRow>
                  <CCol>
                    <CInputGroup>
                      변경 : &nbsp;
                      <FileUpload
                        :id="`post-file-${file.pk}`"
                        v-model="form.oldFiles[i].newFile"
                        size="sm"
                        type="file"
                        @input="enableStore"
                      />
                      <CInputGroupText id="basic-addon2" class="py-0">
                        <CFormCheck
                          :id="`del-file-${file.pk}`"
                          v-model="form.oldFiles[i].del"
                          :value="false"
                          label="삭제"
                          :disabled="!!form.oldFiles[i].newFile"
                          @input="enableStore"
                        />
                      </CInputGroupText>
                    </CInputGroup>
                  </CCol>
                </CRow>
              </small>
            </CCol>
          </CAlert>
        </CRow>

        <CRow class="mb-2">
          <CCol>
            <CInputGroup
              v-for="fNum in newFileRange"
              :key="`fn-${fNum}`"
              class="mb-2"
            >
              <FileUpload
                :id="`file-${fNum}`"
                v-model="form.newFiles[fNum]"
                type="file"
                @input="enableStore"
              />
              <CInputGroupText id="basic-addon2" @click="ctlFileNum(fNum)">
                <v-icon
                  :icon="`mdi-${
                    fNum + 1 < newFileNum ? 'minus' : 'plus'
                  }-thick`"
                  :color="fNum + 1 < newFileNum ? 'error' : 'primary'"
                />
              </CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <CRow>
      <CCol class="text-right">
        <CButton
          color="light"
          @click="$router.push({ name: '본사 소송 문서' })"
        >
          목록으로
        </CButton>
        <CButton
          v-if="route.params.postId"
          color="light"
          @click="$router.go(-1)"
        >
          뒤로
        </CButton>
        <CButton :color="btnClass" type="submit" :disabled="formsCheck">
          저장하기
        </CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="delModal">
    <template #header> 본사 소송 문서</template>
    <template #default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template #footer>
      <CButton color="danger" disabled="">삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="confirmModal">
    <template #header> 본사 소송 문서</template>
    <template #default> 본사 소송 문서 저장을 진행하시겠습니까?</template>
    <template #footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
