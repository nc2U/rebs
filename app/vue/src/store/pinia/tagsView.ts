import { ref } from 'vue'
import { defineStore } from 'pinia'
import { CachedViews, VisitedView } from '@/store/types/tagsView'
import { RouteLocationNormalizedLoaded as RouteNormal } from 'vue-router'

export const useTagsView = defineStore('tags-view', () => {
  // state & getters
  const visitedViews = ref<VisitedView[]>([])
  const cachedViews = ref<CachedViews[]>([])

  // actions
  const addView = (view: VisitedView) => {
    addVisitedView(view)
    addCachedView(view)
  }

  const addVisitedView = (view: VisitedView) => {
    if (visitedViews.value.some(v => v.meta.title === view.meta.title)) return
    visitedViews.value.push(Object.assign({}, view))
  }

  const addCachedView = (view: VisitedView) => {
    if (cachedViews.value.includes(view.name)) return
    if (!view.meta.noCache) cachedViews.value.push(view.name)
  }

  const delView = (view: VisitedView) =>
    new Promise(resolve => {
      delVisitedView(view).then(() => delCachedView(view))
      resolve({
        visitedViews: [...visitedViews.value],
        cachedViews: [...cachedViews.value],
      })
    })

  const delVisitedView = (view: VisitedView) =>
    new Promise(resolve => {
      for (const [i, v] of visitedViews.value.entries()) {
        if (v.path === view.path) {
          visitedViews.value.splice(i, 1)
          break
        }
      }
      resolve([...visitedViews.value])
    })

  const delCachedView = (view: VisitedView) =>
    new Promise(resolve => {
      const index = cachedViews.value.indexOf(view.name)
      index > -1 && cachedViews.value.splice(index, 1)
      resolve([...cachedViews.value])
    })

  const delOthersViews = (view: VisitedView) =>
    new Promise(resolve => {
      delOthersVisitedViews(view).then(() => delOthersCachedViews(view))
      resolve({
        visitedViews: [...visitedViews.value],
        cachedViews: [...cachedViews.value],
      })
    })

  const delOthersVisitedViews = (view: VisitedView) =>
    new Promise(resolve => {
      visitedViews.value = visitedViews.value.filter(v => v.meta.affix || v.path === view.path)
      resolve([...visitedViews.value])
    })

  const delOthersCachedViews = (view: VisitedView) =>
    new Promise(resolve => {
      const index = cachedViews.value.indexOf(view.name)
      if (index > -1) cachedViews.value = cachedViews.value.slice(index, index + 1)
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

  const updateVisitedView = (route: RouteNormal) => {
    for (let v of visitedViews.value) {
      if (v.path === route.path) {
        v = Object.assign(v, route)
        break
      }
    }
  }

  return {
    visitedViews,
    cachedViews,

    addView,
    addVisitedView,
    delView,
    delOthersViews,
    delAllViews,
    updateVisitedView,
  }
})
