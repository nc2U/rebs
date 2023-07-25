<script lang="ts" setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useStore } from 'vuex'
import { useTagsView } from '@/store/pinia/tagsView'
import { VisitedView } from '@/store/types/tagsView'
import {
  useRoute,
  useRouter,
  RouteRecordRaw,
  RouteLocationMatched,
} from 'vue-router'
import { vi } from 'vuetify/locale'

const store = useStore()
const dark = computed(() => store.state.theme === 'dark')
const btnColor = computed(() => (dark.value ? 'blue-grey' : ''))

const [route, router] = [useRoute(), useRouter()]
watch(route, () => {
  addTags()
  moveToCurrentTag()
})

const visible = ref(false)
watch(visible, value =>
  value
    ? document.body.addEventListener('click', closeMenu)
    : document.body.removeEventListener('click', closeMenu),
)

const affixTags = ref<VisitedView[]>([]) // 고정 태그

const currentTag = ref()
const scrollPane = ref()

const tagsViewStore = useTagsView()
const visitedViews = computed(() => tagsViewStore.visitedViews)

const isActive = (currView: VisitedView) =>
  currView.name === route.name || currView.meta.title === route.meta.title

const isAffix = (view: VisitedView) => view.meta && view.meta.affix

const slashPath = (p: string) => (p.charAt(0) !== '/' ? '/' + p : p)

const filterAffixTags = (
  regRoutes: RouteLocationMatched[] | RouteRecordRaw[],
) => {
  let affixedViews: VisitedView[] = []
  regRoutes.forEach((view: RouteLocationMatched | RouteRecordRaw) => {
    if (view.meta && view.meta.affix) {
      const path = slashPath(view.path)
      affixedViews.push({
        name: view.name as string,
        path,
        fullPath: path,
        meta: { ...view.meta },
      })
    }

    if (view.children) {
      const tempViews = filterAffixTags(view.children)
      if (tempViews.length >= 1) {
        affixedViews = [...affixedViews, ...tempViews]
      }
    }
  })
  return affixedViews
}

const initTags = () => {
  affixTags.value = filterAffixTags(route.matched)
  affixTags.value.forEach((tag: VisitedView) =>
    tag.meta.title ? tagsViewStore.addView(tag) : undefined,
  )
}

const addTags = () =>
  route.meta.title && !route.meta.except
    ? tagsViewStore.addView({
        name: route.name,
        path: route.path,
        fullPath: route.fullPath,
        meta: route.meta,
      } as VisitedView)
    : false

const moveToCurrentTag = () =>
  nextTick(() => {
    for (const tag of currentTag.value) {
      if (tag.to.path === route.path) {
        // when query is different then update
        if (tag.to.fullPath !== route.fullPath)
          tagsViewStore.updateVisitedView(route)
        break
      }
    }
  })

const toLastView = () => {
  const latestView = visitedViews.value.slice(-1)[0]
  router.push({ path: latestView.fullPath })
}

const closeSelectedTag = (view: VisitedView) =>
  tagsViewStore.delView(view).then(() => {
    if (isActive(view)) toLastView() // 현재 페이지를 닫았다면 이전 페이지로 이동
  })

const closeMenu = () => (visible.value = false)

onMounted(() => {
  initTags()
  addTags()
})
</script>

<template>
  <v-sheet max-width="100%" class="my-1" :class="{ dark }">
    <v-slide-group show-arrows>
      <v-slide-group-item
        v-for="view in visitedViews"
        :key="view.path"
        ref="scrollPane"
        class="tags-view-item"
        @click.middle="!isAffix(view) ? closeSelectedTag(view) : ''"
      >
        <v-btn
          ref="currentTag"
          class="mx-1 my-0 text-body"
          :class="{ darkBtn: dark }"
          style="text-decoration: none"
          size="small"
          :border="true"
          :rounded="0"
          :color="isActive(view) ? 'success' : btnColor"
          :to="{ path: view.fullPath }"
        >
          <v-icon
            v-if="isActive(view)"
            icon="mdi-circle"
            size="x-small"
            class="mr-2"
          />
          {{ view.meta.title }}
          <v-icon
            v-if="!isAffix(view)"
            icon="mdi-close"
            size="x-small"
            class="pa-2 ml-1 close"
            @click.prevent.stop="closeSelectedTag(view)"
          />
        </v-btn>
      </v-slide-group-item>
    </v-slide-group>
  </v-sheet>
</template>

<style lang="scss" scoped>
.close:hover {
  background: #ccc;
}

.dark {
  background: #2a2b36;
}
</style>
