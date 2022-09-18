<script lang="ts" setup="">
import { computed, onBeforeMount, ref } from 'vue'
import { Post } from '@/store/types/document'
import { write_company_docs } from '@/utils/pageAuth'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  post: { type: Object, default: null },
  categoryList: { type: Object, default: null },
})

const delModal = ref()
const alertModal = ref()
const confirmModal = ref()

const form = ref<Post>({
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
  ip: '',
  device: '',
  secret: false,
  password: '',
  links: [],
  files: [],
})
const validated = ref(false)
const sortName = computed(() =>
  props.post && props.post.project ? props.post.project : '본사',
)

const onSubmit = (event: Event) => {
  if (write_company_docs) {
    const el = event.currentTarget as HTMLFormElement
    if (!el.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else confirmModal.value.callModal()
  } else alertModal.value.callModal()
}

onBeforeMount(() => {
  if (props.post) {
    form.value.pk = props.post.pk
    form.value.board = props.post.board
    form.value.is_notice = props.post.is_notice
    form.value.project = props.post.project
    form.value.category = props.post.category
    form.value.lawsuit = props.post.lawsuit
    form.value.title = props.post.title
    form.value.execution_date = props.post.execution_date
    form.value.content = props.post.content
    form.value.is_hide_comment = props.post.is_hide_comment
    form.value.hit = props.post.hit
    form.value.like = props.post.like
    form.value.dislike = props.post.dislike
    form.value.blame = props.post.blame
    form.value.blame = props.post.blame
    form.value.device = props.post.device
    form.value.secret = props.post.secret
    form.value.password = props.post.password
    form.value.links = props.post.links
    form.value.files = props.post.files
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
        <CFormTextarea
          v-model="form.content"
          placeholder="본문 내용"
          required
          rows="15"
        />
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
        <CButton
          :color="$route.params.postId ? 'success' : 'primary'"
          type="submit"
        >
          저장하기
        </CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="delModal">
    <template #header>
      <CIcon name="cilChevronCircleRightAlt" />
      회사정보
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
