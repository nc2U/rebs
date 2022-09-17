import api from '@/api'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import { PatchPost, Post } from '@/store/types/document'

export type PostFilter = {
  board: number
  is_notice?: boolean
  project?: number
  category?: number
  lawsuit?: number
}

export const useDocument = defineStore('document', () => {
  // state & getters
  const groupList = ref()

  const fetchGroupList = () =>
    api
      .get('/group/')
      .then(res => (groupList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createGroup = () => 2
  const updateGroup = () => 3
  const deleteGroup = () => 4

  const board = ref()
  const boardList = ref()

  const fetchBoard = (pk: number) =>
    api
      .get(`/board/${pk}`)
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

  const categoryList = ref()

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

  const post = ref()
  const postList = ref()
  const postCount = ref(0)

  const postPages = (itemsPerPage: number) =>
    Math.ceil(postCount.value / itemsPerPage)

  const fetchPost = (pk: number) =>
    api
      .get(`/post/${pk}`)
      .then(res => (post.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchPostList = (payload: PostFilter) => {
    const { board, category } = payload

    return api
      .get(`/post/?board=${board || ''}&category=${category || ''}`)
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

  const link = ref()

  const fetchLink = () => 1
  const createLink = () => 2
  const updateLink = () => 3
  const deleteLink = () => 4

  const file = ref()

  const fetchFile = () => 1
  const createFile = () => 2
  const updateFile = () => 3
  const deleteFile = () => 4

  const comment = ref()

  const fetchComment = () => 1
  const createComment = () => 2
  const updateComment = () => 3
  const deleteComment = () => 4

  const tag = ref()

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
    createLink,
    updateLink,
    deleteLink,

    file,

    fetchFile,
    createFile,
    updateFile,
    deleteFile,

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
