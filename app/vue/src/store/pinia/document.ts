import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import {
  Group,
  Board,
  Category,
  AFile,
  Link,
  PatchPost,
  SuitCase,
  SimpleSuitCase,
  Post,
} from '@/store/types/document'

export type SuitCaseFilter = {
  page?: number
  is_com?: '' | boolean
  project?: '' | number
  sort?: '' | '1' | '2' | '3' | '4' | '5'
  level?: '' | '0' | '1' | '2' | '3'
  court?: string
  search?: string
}

export type PostFilter = {
  board?: number
  is_notice?: boolean
  is_com?: boolean
  project?: string
  category?: number | null
  lawsuit?: number
  ordering?: string
  search?: string
  page?: number
}

export const useDocument = defineStore('document', () => {
  // state & getters
  const groupList = ref<Group[]>([])

  const fetchGroupList = () =>
    api
      .get('/group/')
      .then(res => (groupList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createGroup = () => 2
  const updateGroup = () => 3
  const deleteGroup = () => 4

  const board = ref<Board | null>(null)
  const boardList = ref<Board[]>([])

  const fetchBoard = (pk: number) =>
    api
      .get(`/board/${pk}/`)
      .then(res => (board.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchBoardList = () =>
    api
      .get('/board/')
      .then(res => (boardList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createBoard = () => 2
  const updateBoard = () => 3
  const deleteBoard = () => 4

  const categoryList = ref<Category[]>([])

  const fetchCategoryList = (board: number) =>
    api
      .get(`/category/?board=${board}`)
      .then(res => (categoryList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createCategory = () => 2
  const updateCategory = () => 3
  const deleteCategory = () => 4

  const suitcase = ref<SuitCase | null>(null)
  const suitcaseList = ref<SuitCase[]>([])
  const suitcaseCount = ref<number>(0)
  const allSuitCaseList = ref<SimpleSuitCase[]>([])

  const getSuitCase = computed(() =>
    allSuitCaseList.value.map(s => ({
      value: s.pk,
      label: s.__str__
        .replace('지방법원', '지법')
        .replace('고등법원', '고법')
        .replace('대법원', '대법'),
    })),
  )

  const postCases = (itemsPerPage: number) =>
    Math.ceil(suitcaseCount.value / itemsPerPage)

  const fetchSuitCase = (pk: number) =>
    api
      .get(`/suitcase/${pk}/`)
      .then(res => (suitcase.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchSuitCaseList = (payload: SuitCaseFilter) => {
    const page = payload.page || 1
    let queryStr = ''
    if (payload.is_com) queryStr += `&is_com=${payload.is_com}`
    if (payload.project) queryStr += `&project=${payload.project}`
    if (payload.sort) queryStr += `&sort=${payload.sort}`
    if (payload.level) queryStr += `&level=${payload.level}`
    if (payload.court) queryStr += `&court=${payload.court}`

    return api
      .get(`/suitcase/?page=${page}${queryStr}`)
      .then(res => {
        suitcaseList.value = res.data.results
        suitcaseCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const fetchAllSuitCaseList = (payload: SuitCaseFilter) => {
    let queryStr = '?i=1'
    if (payload.is_com) queryStr += `&is_com=${payload.is_com}`
    if (payload.project) queryStr += `&project=${payload.project}`
    if (payload.sort) queryStr += `&sort=${payload.sort}`
    if (payload.level) queryStr += `&level=${payload.level}`
    if (payload.court) queryStr += `&court=${payload.court}`

    return api
      .get(`/all-suitcase/?${queryStr}`)
      .then(res => (allSuitCaseList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const createSuitCase = (payload: SuitCase) =>
    api
      .post(`/suitcase/`, payload)
      .then(() =>
        fetchAllSuitCaseList({}).then(() =>
          fetchSuitCaseList({}).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateSuitCase = (payload: SuitCase) =>
    api
      .put(`/suitcase/${payload.pk}/`, payload)
      .then(() =>
        fetchAllSuitCaseList({}).then(() =>
          fetchSuitCaseList({}).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const deleteSuitCase = (pk: number) =>
    api
      .delete(`/suitcase/${pk}/`)
      .then(() =>
        fetchAllSuitCaseList({}).then(() =>
          fetchSuitCaseList({}).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const post = ref<Post | null>(null)
  const postList = ref<Post[]>([])
  const postCount = ref(0)

  const postPkList = computed(() => postList.value.map(p => p.pk))
  const postPk = computed(() => post.value?.pk || 0)
  const postIndex = computed(() => postPkList.value.indexOf(postPk.value))

  const getPrev = computed(() =>
    postIndex.value && postIndex.value === postList.value.length
      ? null
      : postPkList.value[postIndex.value + 1],
  )

  const getNext = computed(() =>
    postIndex.value && postIndex.value === 0
      ? null
      : postPkList.value[postIndex.value - 1],
  )

  const postPages = (itemsPerPage: number) =>
    Math.ceil(postCount.value / itemsPerPage)

  const fetchPost = (pk: number) =>
    api
      .get(`/post/${pk}/`)
      .then(res => (post.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchPostList = (payload: PostFilter) => {
    const { board, page } = payload
    let url = `/post/?board=${board}&page=${page || 1}`
    if (payload.is_com) url += `&is_com=${payload.is_com}`
    if (payload.project) url += `&project=${payload.project}`
    if (payload.category) url += `&category=${payload.category}`
    if (payload.lawsuit) url += `&lawsuit=${payload.lawsuit}`
    if (payload.ordering) url += `&ordering=${payload.ordering}`
    if (payload.search) url += `&search=${payload.search}`

    return api
      .get(url)
      .then(res => {
        postList.value = res.data.results
        postCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createPost = (payload: { form: FormData }) =>
    api
      .post(`/post/`, payload.form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      .then(res =>
        fetchPostList({ board: res.data.board }).then(() => message()),
      )
      .catch(err => errorHandle(err.response.data))

  const updatePost = (payload: { pk: number; form: FormData }) =>
    api
      .put(`/post/${payload.pk}/`, payload.form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      .then(() => message())
      .catch(err => errorHandle(err.response.data))

  const patchPost = (payload: PatchPost) =>
    api
      .patch(`/post/${payload.pk}/`, payload)
      .then(res => fetchPost(res.data.pk))
      .catch(err => errorHandle(err.response.data))

  const deletePost = () => 4

  const link = ref<Link | null>(null)

  const fetchLink = (pk: number) =>
    api
      .get(`/link/${pk}/`)
      .then(res => (link.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const patchLink = (payload: Link) =>
    api
      .patch(`/link/${payload.pk}/`, payload)
      .then(res => fetchPost(res.data.post))
      .catch(err => errorHandle(err.response.data))

  const file = ref<AFile | null>(null)

  const fetchFile = (pk: number) =>
    api
      .get(`/file/${pk}/`)
      .then(res => (file.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const patchFile = (payload: AFile) =>
    api
      .patch(`/file/${payload.pk}/`, payload)
      .then(res => fetchPost(res.data.post))
      .catch(err => errorHandle(err.response.data))

  const comment = ref(null)

  const fetchComment = () => 1
  const createComment = () => 2
  const updateComment = () => 3
  const deleteComment = () => 4

  const tag = ref(null)

  const fetchTag = () => 1
  const createTag = () => 2
  const updateTag = () => 3
  const deleteTag = () => 4

  return {
    groupList,

    fetchGroupList,
    createGroup,
    updateGroup,
    deleteGroup,

    board,
    boardList,

    fetchBoard,
    fetchBoardList,
    createBoard,
    updateBoard,
    deleteBoard,

    categoryList,

    fetchCategoryList,
    createCategory,
    updateCategory,
    deleteCategory,

    suitcase,
    suitcaseList,
    suitcaseCount,
    getSuitCase,

    postCases,
    fetchSuitCase,
    fetchSuitCaseList,
    fetchAllSuitCaseList,
    createSuitCase,
    updateSuitCase,
    deleteSuitCase,

    post,
    postList,
    postCount,
    getPrev,
    getNext,

    postPages,
    fetchPost,
    fetchPostList,
    createPost,
    updatePost,
    patchPost,
    deletePost,

    link,
    fetchLink,
    patchLink,

    file,
    fetchFile,
    patchFile,

    comment,

    fetchComment,
    createComment,
    updateComment,
    deleteComment,

    tag,

    fetchTag,
    createTag,
    updateTag,
    deleteTag,
  }
})
