<script lang="ts" setup>
import { ref, reactive, computed, onMounted, onUpdated, type PropType } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Post, Link, Category } from '@/store/types/document'
import { AlertSecondary } from '@/utils/cssMixins'
import QuillEditor from '@/components/QuillEditor/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  categoryList: { type: Object as PropType<Category[]>, default: () => [] },
  post: { type: Object as PropType<Post>, default: null },
  viewRoute: { type: String, required: true },
  writeAuth: { type: Boolean, default: true },
})

const emit = defineEmits(['on-submit', 'file-upload', 'file-change', 'close'])

const refDelModal = ref()
const refAlertModal = ref()
const refConfirmModal = ref()

const attach = ref(true)
const validated = ref(false)
const form = reactive<Post>({
  pk: undefined,
  company: null,
  project: null,
  board: 1,
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
  links: [],
  files: [],
})

const newLinks = ref<Link[]>([])

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

const [route, router] = [useRoute(), useRouter()]
const btnClass = computed(() => (route.params.postId ? 'success' : 'primary'))

const range = (from: number, to: number): number[] =>
  from < to ? [from, ...range(from + 1, to)] : []

const newLinkNum = ref(1)
const newLinkRange = computed(() => range(0, newLinkNum.value))

const newFileNum = ref(1)
const newFileRange = computed(() => range(0, newFileNum.value))

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

const fileChange = (event: Event, pk: number) => {
  enableStore(event)
  const el = event.target as HTMLInputElement
  if (el.files) {
    const file = el.files[0]
    emit('file-change', { pk, file })
  }
}

const fileUpload = (event: Event) => {
  enableStore(event)
  const el = event.target as HTMLInputElement
  if (el.files) {
    const file = el.files[0]
    emit('file-upload', file)
  }
}

const onSubmit = (event: Event) => {
  if (props.writeAuth) {
    const el = event.currentTarget as HTMLFormElement
    if (!el.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else refConfirmModal.value.callModal()
  } else refAlertModal.value.callModal()
}

const modalAction = () => {
  emit('on-submit', { ...form, newLinks: newLinks.value })
  validated.value = false
  refConfirmModal.value.close()
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
    form.links = props.post.links
    form.files = props.post.files
  }
}

onMounted(() => dataSetup())
onUpdated(() => dataSetup())
</script>

<template>
  <CForm
    enctype="multipart/form-data"
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="mb-3">
      <CFormLabel for="title" class="col-md-2 col-form-label">제목</CFormLabel>
      <CCol md="8">
        <CFormInput id="title" v-model="form.title" required placeholder="게시물 제목" />
      </CCol>
      <CCol md="2">
        <v-checkbox-btn v-model="form.is_notice" label="공지글" />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="category" class="col-sm-2 col-form-label"> 카테고리</CFormLabel>
      <CCol md="3">
        <CFormSelect id="category" v-model="form.category">
          <option value="">카테고리 선택</option>
          <option v-for="cate in categoryList" :key="cate.pk ?? 0" :value="cate.pk ?? 0">
            {{ cate.name }}
          </option>
        </CFormSelect>
      </CCol>

      <!--      <CFormLabel for="inputPassword" class="col-sm-2 col-form-label"> 문서 발행일자</CFormLabel>-->
      <!--      <CCol md="3">-->
      <!--        <DatePicker v-model="form.execution_date" placeholder="문서 발행일자" />-->
      <!--      </CCol>-->
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="title" class="col-md-2 col-form-label">내용</CFormLabel>
      <CCol md="10 mb-5">
        <QuillEditor v-model:content="form.content" placeholder="본문 내용" />
      </CCol>
    </CRow>

    <CRow>
      <CFormLabel for="title" class="col-md-2 col-form-label">링크</CFormLabel>
      <CCol md="10" lg="8" xl="6">
        <CRow v-if="post && form.links?.length">
          <CAlert :color="AlertSecondary">
            <CCol>
              <CInputGroup v-for="(link, i) in form.links" :key="link.pk" class="mb-2">
                <CFormInput
                  :id="`post-link-${link.pk}`"
                  v-model="form.links[i].link"
                  size="sm"
                  placeholder="파일 링크"
                  @input="enableStore"
                />
                <CInputGroupText id="basic-addon1" class="py-0">
                  <CFormCheck
                    :id="`del-link-${link.pk}`"
                    v-model="form.links[i].del"
                    :value="true"
                    @input="enableStore"
                    label="삭제"
                  />
                </CInputGroupText>
              </CInputGroup>
            </CCol>
          </CAlert>
        </CRow>

        <CRow class="mb-2">
          <CCol>
            <CInputGroup v-for="lNum in newLinkRange" :key="`ln-${lNum}`" class="mb-2">
              <CFormInput
                :id="`link-${lNum}`"
                v-model="newLinks[lNum]"
                placeholder="파일 링크"
                @input="enableStore"
              />
              <CInputGroupText id="basic-addon1" @click="ctlLinkNum(lNum)">
                <v-icon
                  :icon="`mdi-${lNum + 1 < newLinkNum ? 'minus' : 'plus'}-thick`"
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
        <CRow v-if="post && form.files?.length">
          <CAlert :color="AlertSecondary">
            <small>{{ devideUri(form.files[0].file ?? ' ')[0] }}</small>
            <CCol v-for="(file, i) in form.files" :key="file.pk" xs="12" color="primary">
              <small>
                현재 :
                <a :href="file.file" target="_blank">
                  {{ devideUri(file.file ?? ' ')[1] }}
                </a>
                <CRow>
                  <CCol>
                    <CInputGroup>
                      변경 : &nbsp;
                      <CFormInput
                        :id="`post-file-${file.pk}`"
                        v-model="form.files[i].newFile"
                        size="sm"
                        type="file"
                        @input="fileChange($event, file.pk as number)"
                      />
                      <CInputGroupText id="basic-addon2" class="py-0">
                        <input
                          :id="`del-file-${file.pk}`"
                          v-model="form.files[i].del"
                          :value="true"
                          :disabled="!!form.files[i].newFile"
                          @input="enableStore"
                          type="checkbox"
                          class="form-check-input mr-1"
                        />
                        <label :for="`del-file-${file.pk}`" class="form-label form-check-label">
                          삭제
                        </label>
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
            <CInputGroup v-for="fNum in newFileRange" :key="`fn-${fNum}`" class="mb-2">
              <CFormInput :id="`file-${fNum}`" type="file" @input="fileUpload" />
              <CInputGroupText id="basic-addon2" @click="ctlFileNum(fNum)">
                <v-icon
                  :icon="`mdi-${fNum + 1 < newFileNum ? 'minus' : 'plus'}-thick`"
                  :color="fNum + 1 < newFileNum ? 'error' : 'primary'"
                />
              </CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <v-divider />

    <CRow>
      <CCol class="text-right">
        <CButton color="light" @click="router.push({ name: '공지 사항' })"> 목록으로</CButton>
        <CButton v-if="route.params.postId" color="light" @click="router.go(-1)"> 뒤로</CButton>
        <CButton :color="btnClass" type="submit" :disabled="formsCheck"> 저장하기</CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="refDelModal">
    <template #header> {{ viewRoute }}</template>
    <template #default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template #footer>
      <CButton color="danger" disabled>삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="refConfirmModal">
    <template #header> {{ viewRoute }}</template>
    <template #default> {{ viewRoute }} 저장을 진행하시겠습니까?</template>
    <template #footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="refAlertModal" />
</template>
