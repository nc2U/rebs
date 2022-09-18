<script lang="ts" setup="">
import { ref, reactive, computed, onBeforeMount, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useDocument } from '@/store/pinia/document'
import { Post } from '@/store/types/document'
import { write_company_docs } from '@/utils/pageAuth'
import Editor from '@/components/TinyMce/index.vue'
// import Tiptap from '@/components/TipTap/index.vue'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  categoryList: { type: Object, default: null },
})

const emit = defineEmits(['on-submit', 'close'])

const delModal = ref()
const alertModal = ref()
const confirmModal = ref()

const form = reactive<Post>({
  pk: null,
  board: null,
  is_notice: false,
  project: null,
  category: null,
  lawsuit: null,
  title: '',
  execution_date: '',
  content: '',
  is_hide_comment: false,
  hit: 0,
  like: 0,
  dislike: 0,
  blame: 0,
  ip: null,
  device: '',
  secret: false,
  password: '',
  links: [],
  files: [],
})

const validated = ref(false)

const documentStore = useDocument()
const post = computed(() => documentStore.post)

const sortName = computed(() =>
  post.value && post.value.project ? post.value.proj_name : '본사',
)

const fetchPost = (pk: number) => documentStore.fetchPost(pk)

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
  emit('on-submit', { ...form })
  validated.value = false
  confirmModal.value.close()
}

onBeforeMount(() => {
  if (route.params.postId) fetchPost(Number(route.params.postId))
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
    form.like = val.like
    form.dislike = val.dislike
    form.blame = val.blame
    form.blame = val.blame
    form.device = val.device
    form.secret = val.secret
    form.password = val.password
    form.links = val.links
    form.files = val.files
  }
})
</script>

<template>
  <CRow class="mt-5">
    <CCol>
      <h5>
        {{ sortName }}
        <v-icon icon="mdi-chevron-double-right" size="xs" />
        일반문서
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
      <CCol md="8">
        <CFormInput
          id="title"
          v-model="form.title"
          required
          placeholder="게시물 제목"
        />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="category" class="col-sm-2 col-form-label">
        카테고리
      </CFormLabel>
      <CCol md="3">
        <CFormSelect id="category" v-model="form.category" required>
          <option value="">카테고리 선택</option>
          <option v-for="cate in categoryList" :key="cate.pk" :value="cate.pk">
            {{ cate.name }}
          </option>
        </CFormSelect>
      </CCol>

      <CFormLabel for="inputPassword" class="col-sm-2 col-form-label">
        문서 시행일자
      </CFormLabel>
      <CCol md="3">
        <DatePicker v-model="form.execution_date" placeholder="문서 시행일자" />
      </CCol>
      <CCol class="pt-2">
        <CFormSwitch id="is_notice" v-model="form.is_notice" label="공지여부" />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="title" class="col-md-2 col-form-label">내용</CFormLabel>
      <CCol md="10">
        <Editor v-model="form.content" placeholder="본문 내용" rows="20" />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="title" class="col-md-2 col-form-label">링크</CFormLabel>
      <CCol md="6">
        <CInputGroup>
          <CFormInput
            id="title"
            v-model="form.links[0]"
            placeholder="파일 링크"
            aria-label="File Link"
            aria-describedby="basic-addon1"
          />
          <CInputGroupText id="basic-addon1">+</CInputGroupText>
        </CInputGroup>
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="title" class="col-md-2 col-form-label">파일</CFormLabel>
      <CCol md="6">
        <CInputGroup>
          <CFormInput
            id="title"
            v-model="form.files[0]"
            type="file"
            aria-label="File"
            aria-describedby="basic-addon2"
          />
          <CInputGroupText id="basic-addon2">+</CInputGroupText>
        </CInputGroup>
      </CCol>
    </CRow>

    <CRow>
      <CCol class="text-right">
        <CButton color="light" @click="$router.push({ name: '본사 일반문서' })">
          목록으로
        </CButton>
        <CButton :color="btnClass" type="submit">저장하기</CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="delModal">
    <template #header>
      <CIcon name="cilChevronCircleRightAlt" />
      본사 일반문서
    </template>
    <template #default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template #footer>
      <CButton color="danger" disabled="">삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cilChevronCircleRightAlt" />
      본사 일반문서
    </template>
    <template #default> 본사 일반문서 저장을 진행하시겠습니까?</template>
    <template #footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
