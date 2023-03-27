<script lang="ts" setup>
import {ref, reactive, computed, onBeforeMount, watch} from 'vue'
import {onBeforeRouteLeave, useRoute} from 'vue-router'
import {useDocument, SuitCaseFilter} from '@/store/pinia/document'
import {Post, Attatches} from '@/store/types/document'
import {write_company_docs} from '@/utils/pageAuth'
import {dateFormat} from '@/utils/baseMixins'
import {AlertSecondary} from '@/utils/cssMixins'
import ToastEditor from '@/components/ToastEditor/index.vue'
import FileUpload from '@/components/FileUpload.vue'
import DatePicker from '@/components/DatePicker/index.vue'
import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({categoryList: {type: Object, default: null}})

const emit = defineEmits(['on-submit', 'close'])

const delModal = ref()
const alertModal = ref()
const confirmModal = ref()

const form = reactive<Post & Attatches>({
  pk: null,
  company: null,
  project: null,
  board: 2,
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

const ctlLinkNum = (n: number) => {
  if (n + 1 >= newLinkNum.value) newLinkNum.value = newLinkNum.value + 1
  else newLinkNum.value = newLinkNum.value - 1
}

const ctlFileNum = (n: number) => {
  if (n + 1 >= newFileNum.value) newFileNum.value = newFileNum.value + 1
  else newFileNum.value = newFileNum.value - 1
}

const validated = ref(false)

const documentStore = useDocument()
const post = computed(() => documentStore.post)
const getSuitCase = computed(() => documentStore.getSuitCase)

const attach = ref(true)

const formsCheck = computed(() => {
  if (post.value) {
    const a = form.is_notice === post.value.is_notice
    const b = form.category === post.value.category
    const c = form.lawsuit === post.value.lawsuit
    const d = form.title === post.value.title
    const e = form.execution_date === post.value.execution_date
    const f = form.content === post.value.content

    return a && b && c && d && e && f && attach.value
  } else return false
})

const enableStore = (event: Event) => {
  const el = event.target as HTMLInputElement
  attach.value = !el.value
}

const sortName = computed(() =>
    post.value && post.value.project ? post.value.proj_name : '본사',
)

const fetchPost = (pk: number) => documentStore.fetchPost(pk)
const fetchAllSuitCaseList = (payload: SuitCaseFilter) =>
    documentStore.fetchAllSuitCaseList(payload)

const route = useRoute()
const btnClass = computed(() => (route.params.postId ? 'success' : 'primary'))

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
  emit('on-submit', {...form})
  validated.value = false
  confirmModal.value.close()
}

const devideUri = (uri: string) => {
  const devidedUri = decodeURI(uri).split('media/')
  return [devidedUri[0] + 'media/', devidedUri[1]]
}

watch(form, val => {
  if (val.execution_date) form.execution_date = dateFormat(val.execution_date)
})

watch(post, val => {
  if (val) {
    form.pk = val.pk
    form.board = val.board
    form.is_notice = val.is_notice
    form.project = val.project
    form.category = val.category
    form.lawsuit = val.lawsuit
    form.title = val.title
    form.execution_date = val.execution_date
    form.content = val.content
    form.is_hide_comment = val.is_hide_comment
    form.hit = val.hit
    form.blame = val.blame
    form.blame = val.blame
    form.device = val.device
    form.secret = val.secret
    form.password = val.password
    if (val.links) form.oldLinks = val.links
    if (val.files) {
      form.oldFiles = val.files.map(file => ({
        pk: file.pk,
        file: file.file,
        newFile: '',
        hit: file.hit,
      }))
    }
  }
})

watch(route, val => {
  if (val.params.postId) fetchPost(Number(val.params.postId))
  else documentStore.post = null
})

onBeforeMount(() => {
  if (route.params.postId) fetchPost(Number(route.params.postId))
  fetchAllSuitCaseList({})
})

onBeforeRouteLeave(() => {
  documentStore.post = null
})
</script>

<template>
  <CRow class="mt-5">
    <CCol>
      <h5>
        {{ sortName }}
        <v-icon icon="mdi-chevron-double-right" size="xs"/>
        소송 문서
      </h5>
    </CCol>
  </CRow>

  <hr/>

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
        <ToastEditor v-model="form.content" placeholder="본문 내용"/>
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

  <AlertModal ref="alertModal"/>
</template>
