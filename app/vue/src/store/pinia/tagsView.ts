import { ref } from 'vue'
import { defineStore } from 'pinia'
import { CachedViews, VisitedViews } from '@/store/types/tagsView'

export const useTagsView = defineStore('tagsView', () => {
  // state & getters
  const visitedViews = ref<VisitedViews[]>([])
  const cachedViews = ref<CachedViews[]>([])

  // actions
  const addView = (view: any) => {
    addVisitedView(view)
    addCachedView(view)
  }

  const addVisitedView = (view: VisitedViews) => {
    if (visitedViews.value.some(v => v.name === view.name)) return
    visitedViews.value.push(Object.assign({}, view))
  }

  const addCachedView = (view: VisitedViews) => {
    if (cachedViews.value.includes(view.name)) return
    if (!view.meta.noCache) cachedViews.value.push(view.name)
  }

  const delView = (view: VisitedViews) =>
    new Promise(resolve => {
      delVisitedView(view).then(() => delCachedView(view))
      resolve({
        visitedViews: [...visitedViews.value],
        cachedViews: [...cachedViews.value],
      })
    })

  const delVisitedView = (view: VisitedViews) =>
    new Promise(resolve => {
      for (const [i, v] of visitedViews.value.entries()) {
        if (v.path === view.path) {
          visitedViews.value.splice(i, 1)
          break
        }
      }
      resolve([...visitedViews.value])
    })

  const delCachedView = (view: VisitedViews) =>
    new Promise(resolve => {
      const index = cachedViews.value.indexOf(view.name)
      index > -1 && cachedViews.value.splice(index, 1)
      resolve([...cachedViews.value])
    })

  const delOthersViews = (view: VisitedViews) =>
    new Promise(resolve => {
      delOthersVisitedViews(view).then(() => delOthersCachedViews(view))
      resolve({
        visitedViews: [...visitedViews.value],
        cachedViews: [...cachedViews.value],
      })
    })

  const delOthersVisitedViews = (view: VisitedViews) =>
    new Promise(resolve => {
      visitedViews.value = visitedViews.value.filter(
        v => v.meta.affix || v.path === view.path,
      )
      resolve([...visitedViews.value])
    })

  const delOthersCachedViews = (view: VisitedViews) =>
    new Promise(resolve => {
      const index = cachedViews.value.indexOf(view.name)
      if (index > -1)
        cachedViews.value = cachedViews.value.slice(index, index + 1)
      else cachedViews.value = []
      resolve([...cachedViews.value])
    })

  const delAllViews = () =>
    new Promise(resolve => {
      delAllVisitedViews().then(() => delAllCachedViews())
      resolve({
        visitedViews: [...visitedViews.value],
        cachedViews: [...cachedViews.value],
      })
    })

  const delAllVisitedViews = () =>
    new Promise(resolve => {
      visitedViews.value = visitedViews.value.filter(tag => tag.meta.affix)
      resolve([...visitedViews.value])
    })

  const delAllCachedViews = () =>
    new Promise(resolve => {
      cachedViews.value = []
      resolve([...cachedViews.value])
    })

  const updateVisitedView = (view: VisitedViews) => {
    for (let v of visitedViews.value) {
      if (v.path === view.path) {
        v = Object.assign(v, view)
        break
      }
    }
  }

  return {
    visitedViews,
    cachedViews,

    addView,
    delView,
    delOthersViews,
    delAllViews,
    updateVisitedView,
  }
})
