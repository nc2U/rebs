import api from '@/api'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import { Category, File, Link, PatchPost, Post } from '@/store/types/document'

export type PostFilter = {
  board: number
  is_notice?: boolean
  project?: number
  category?: number
  lawsuit?: number
  page?: number
}

export const useDocument = defineStore('document', () => {
  // state & getters
  const groupList = ref([])

  const fetchGroupList = () =>
    api
      .get('/group/')
      .then(res => (groupList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createGroup = () => 2
  const updateGroup = () => 3
  const deleteGroup = () => 4

  const board = ref(null)
  const boardList = ref([])

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

  const suitcase = ref()

  const fetchSuitCase = () => 1
  const createSuitCase = () => 2
  const updateSuitCase = () => 3
  const deleteSuitCase = () => 4

  const post = ref<Post | null>(null)
  const postList = ref<Post[]>([])
  const postCount = ref(0)

  const postPages = (itemsPerPage: number) =>
    Math.ceil(postCount.value / itemsPerPage)

  const fetchPost = (pk: number) =>
    api
      .get(`/post/${pk}/`)
      .then(res => (post.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchPostList = (payload: PostFilter) => {
    const { board, category, page } = payload

    return api
      .get(
        `/post/?board=${board || ''}&category=${category || ''}&page=${
          page || 1
        }`,
      )
      .then(res => {
        postList.value = res.data.results
        postCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createPost = (payload: Post) =>
    api
      .post(`/post/`, payload)
      .then(() => message())
      .catch(err => errorHandle(err.response.data))

  const updatePost = (payload: Post) =>
    api
      .put(`/post/${payload.pk}/`, payload)
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

  const file = ref<File | null>(null)

  const fetchFile = (pk: number) =>
    api
      .get(`/file/${pk}/`)
      .then(res => (file.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const patchFile = (payload: File) =>
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

    fetchSuitCase,
    createSuitCase,
    updateSuitCase,
    deleteSuitCase,

    post,
    postList,
    postCount,

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
