import api from '@/api'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import type {
  Group,
  Board,
  Category,
  AFile,
  Link,
  PatchPost,
  SuitCase,
  SimpleSuitCase,
  Post,
  Comment as Cm,
} from '@/store/types/document'
import { useAccount } from '@/store/pinia/account'

export type SuitCaseFilter = {
  company?: number | ''
  project?: number | ''
  is_com?: boolean
  court?: string
  related_case?: number | ''
  sort?: '1' | '2' | '3' | '4' | '5' | ''
  level?: '1' | '2' | '3' | '4' | '5' | '6' | '7' | ''
  in_progress?: boolean | ''
  search?: string
  page?: number
}

export type PostFilter = {
  company?: number | ''
  project?: number | ''
  board?: number
  is_notice?: boolean | ''
  is_com?: boolean
  category?: number | ''
  lawsuit?: number | ''
  user?: number | ''
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
  const getCaseNav = computed(() =>
    suitcaseList.value.map(s => ({
      pk: s.pk,
      prev_pk: s.prev_pk,
      next_pk: s.next_pk,
    })),
  )

  const casePages = (itemsPerPage: number) => Math.ceil(suitcaseCount.value / itemsPerPage)

  const fetchSuitCase = (pk: number) =>
    api
      .get(`/suitcase/${pk}/`)
      .then(res => (suitcase.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const getQueryStr = (payload: SuitCaseFilter) => {
    const { project, is_com, in_progress, court, related_case, sort, level, search } = payload
    let queryStr = ''
    if (project) queryStr += `&project=${project}`
    queryStr += `&is_com=${is_com ?? ''}`
    queryStr += `&in_progress=${in_progress ?? ''}`
    if (court) queryStr += `&court=${court}`
    if (related_case) queryStr += `&related_case=${related_case}`
    if (sort) queryStr += `&sort=${sort}`
    if (level) queryStr += `&level=${level}`
    if (search) queryStr += `&search=${search}`
    return queryStr
  }

  const fetchSuitCaseList = async (payload: SuitCaseFilter) => {
    const page = payload.page ?? 1
    const company = payload.company ?? ''
    const queryStr = getQueryStr(payload)
    return await api
      .get(`/suitcase/?page=${page}&company=${company}${queryStr}`)
      .then(res => {
        suitcaseList.value = res.data.results
        suitcaseCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const fetchAllSuitCaseList = async (payload: SuitCaseFilter) => {
    const queryStr = getQueryStr(payload)
    return await api
      .get(`/all-suitcase/?company=${payload.company ?? ''}&${queryStr}`)
      .then(res => (allSuitCaseList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const createSuitCase = async (
    payload: SuitCase & {
      isProject?: boolean
    },
  ) => {
    const retData: SuitCaseFilter = payload.isProject
      ? { company: payload.company ?? '', is_com: false, project: payload.project ?? '', page: 1 }
      : { company: payload.company ?? '', is_com: true, page: 1 }
    return await api
      .post(`/suitcase/`, payload)
      .then(() =>
        fetchAllSuitCaseList(retData).then(() => fetchSuitCaseList(retData).then(() => message())),
      )
      .catch(err => errorHandle(err.response.data))
  }

  const updateSuitCase = (payload: SuitCase) =>
    api
      .put(`/suitcase/${payload.pk}/`, payload)
      .then(() => message())
      .catch(err => errorHandle(err.response.data))

  const deleteSuitCase = (pk: number) =>
    api
      .delete(`/suitcase/${pk}/`)
      .then(() => fetchAllSuitCaseList({}).then(() => fetchSuitCaseList({}).then(() => message())))
      .catch(err => errorHandle(err.response.data))

  const accStore = useAccount()
  const post = ref<Post | null>(null)
  const postList = ref<Post[]>([])
  const noticeList = ref<Post[]>([])
  const postCount = ref(0)
  const getPostNav = computed(() =>
    postList.value.map(p => ({
      pk: p.pk,
      prev_pk: p.prev_pk,
      next_pk: p.next_pk,
    })),
  )

  const postPages = (itemsPerPage: number) => Math.ceil(postCount.value / itemsPerPage)

  const fetchPost = async (pk: number) =>
    api
      .get(`/post/${pk}/`)
      .then(res => {
        post.value = res.data
        fetchCommentList({ post: pk })
      })
      .catch(err => errorHandle(err.response.data))

  const fetchNoticeList = async (board: number | undefined) => {
    let url = `/post/?is_notice=true`
    url = board ? `${url}&board=${board}` : url
    return await api
      .get(url)
      .then(res => (noticeList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const fetchPostList = async (payload: PostFilter) => {
    const { board, page } = payload
    let url = `/post/?page=${page ?? 1}&is_notice=false`
    if (payload.board) url += `&board=${board}`
    if (payload.company) url += `&company=${payload.company}`
    if (payload.is_com) url += `&is_com=${payload.is_com}`
    if (payload.project) url += `&project=${payload.project}`
    if (payload.category) url += `&category=${payload.category}`
    if (payload.lawsuit) url += `&lawsuit=${payload.lawsuit}`
    if (payload.user) url += `&user=${payload.user}`
    if (payload.ordering) url += `&ordering=${payload.ordering}`
    if (payload.search) url += `&search=${payload.search}`
    await fetchNoticeList(board)

    return await api
      .get(url)
      .then(res => {
        postList.value = res.data.results
        postCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createPost = (
    payload: {
      form: FormData
    } & {
      isProject?: boolean
    },
  ) =>
    api
      .post(`/post/`, payload.form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      .then(res =>
        fetchPostList({
          company: res.data.company,
          project: res.data.project,
          board: res.data.board,
          is_com: !payload.isProject,
          page: 1,
        }).then(() => message()),
      )
      .catch(err => errorHandle(err.response.data))

  const updatePost = (
    payload: {
      pk: number
      form: FormData
    } & {
      isProject?: boolean
    },
  ) =>
    api
      .put(`/post/${payload.pk}/`, payload.form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      .then(res =>
        fetchPostList({
          company: res.data.company,
          project: res.data.project,
          board: res.data.board,
          is_com: !payload.isProject,
          page: 1,
        }).then(() => fetchPost(res.data.pk).then(() => message())),
      )
      .catch(err => errorHandle(err.response.data))

  const patchPost = async (
    payload: PatchPost & {
      filter?: PostFilter
    },
  ) => {
    const { filter, ...data } = payload
    return await api
      .patch(`/post/${data.pk}/`, data)
      .then(res =>
        fetchPostList({
          company: res.data.company,
          ...filter,
        }).then(() => fetchPost(res.data.pk)),
      )
      .catch(err => errorHandle(err.response.data))
  }

  const patchPostLike = (pk: number) =>
    api
      .patch(`/post-like/${pk}/`, { pk })
      .then(() => accStore.fetchProfile().then(() => fetchPost(pk)))
      .catch(err => errorHandle(err.response.data))

  const patchPostBlame = (pk: number) =>
    api
      .patch(`/post-blame/${pk}/`, { pk })
      .then(() => accStore.fetchProfile().then(() => fetchPost(pk)))
      .catch(err => errorHandle(err.response.data))

  const deletePost = (pk: number) =>
    api
      .delete(`/post/${pk}/`)
      .then(() => message('warning'))
      .catch(err => errorHandle(err.response.data))

  // state
  const trashPost = ref<Post | null>(null)
  const trashPostList = ref<Post[]>([])
  const trashPostCount = ref(0)

  const trashPostPages = (itemsPerPage: number) => Math.ceil(trashPostCount.value / itemsPerPage)

  const fetchTrashPost = async (pk: number) =>
    api
      .get(`/post-trash-can/${pk}/`)
      .then(res => {
        trashPost.value = res.data
        fetchCommentList({ post: pk })
      })
      .catch(err => errorHandle(err.response.data))

  const fetchTrashPostList = (page = 1) =>
    api
      .get(`/post-trash-can/?page=${page}`)
      .then(res => {
        trashPostList.value = res.data.results
        trashPostCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))

  const restorePost = (pk: number, isProject = false) =>
    api
      .put(`/post-trash-can/${pk}/`)
      .then(res =>
        fetchPostList({
          company: res.data.company,
          project: res.data.project,
          board: res.data.board,
          is_com: !isProject,
          page: 1,
        }).then(() => fetchTrashPostList().then(() => message())),
      )
      .catch(err => errorHandle(err.response.data))

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

  const comment = ref<Cm | null>(null)
  const commentList = ref<Cm[]>([])
  const commentCount = ref(0)

  const fetchComment = (pk: number) =>
    api
      .get(`/comment/${pk}/`)
      .then(res => (comment.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchCommentList = async (payload: { post?: number; user?: number; page?: number }) => {
    const { post, user, page } = payload
    let url = `/comment/?page=${page ?? 1}`
    url = post ? `${url}&post=${post}&is_comment=true` : url
    url = user ? `${url}&user=${user}` : url

    return await api
      .get(url)
      .then(res => {
        commentList.value = res.data.results
        commentCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createComment = (payload: Cm) =>
    api
      .post(`/comment/`, payload)
      .then(res => fetchPost(res.data.post.pk).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const patchComment = (payload: Cm) =>
    api
      .patch(`/comment/${payload.pk}/`, payload)
      .then(res => fetchPost(res.data.post.pk).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const patchCommentLike = (pk: number, post: number, page = 1) =>
    api
      .patch(`/comment-like/${pk}/`, { pk })
      .then(() => accStore.fetchProfile().then(() => fetchCommentList({ post, page })))
      .catch(err => errorHandle(err.response.data))

  const patchCommentBlame = (pk: number, post: number, page = 1) =>
    api
      .patch(`/comment-blame/${pk}/`, { pk })
      .then(() => accStore.fetchProfile().then(() => fetchCommentList({ post, page })))
      .catch(err => errorHandle(err.response.data))

  const deleteComment = (payload: { pk: number; post: number }) =>
    api
      .delete(`/comment/${payload.pk}/`)
      .then(() => fetchPost(payload.post).then(() => message()))
      .catch(err => errorHandle(err.response.data))

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
    getCaseNav,

    casePages,
    fetchSuitCase,
    fetchSuitCaseList,
    fetchAllSuitCaseList,
    createSuitCase,
    updateSuitCase,
    deleteSuitCase,

    post,
    postList,
    noticeList,
    postCount,
    getPostNav,

    postPages,
    fetchPost,
    fetchPostList,
    createPost,
    updatePost,
    patchPost,
    patchPostLike,
    patchPostBlame,
    deletePost,

    trashPost,
    trashPostList,
    trashPostCount,

    trashPostPages,
    fetchTrashPost,
    fetchTrashPostList,
    restorePost,

    link,
    fetchLink,
    patchLink,

    file,
    fetchFile,
    patchFile,

    comment,
    commentList,
    commentCount,

    fetchComment,
    fetchCommentList,
    createComment,
    patchComment,
    patchCommentLike,
    patchCommentBlame,
    deleteComment,

    tag,

    fetchTag,
    createTag,
    updateTag,
    deleteTag,
  }
})
