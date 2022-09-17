<script lang="ts" setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useStore } from 'vuex'
import { useTagsView } from '@/store/pinia/tagsView'
import { VisitedViews } from '@/store/types/tagsView'
import { RouteRecordRaw, useRoute, useRouter } from 'vue-router'

const [route, router] = [useRoute(), useRouter()]

const routes = route.matched

const store = useStore()
const dark = computed(() => store.state.theme === 'dark')
const btnColor = computed(() => (dark.value ? 'blue-grey' : ''))

const visible = ref(false)
const affixTags = ref<VisitedViews[]>([])

const currentTag = ref()
const scrollPane = ref()

const tagsViewStore = useTagsView()
const visitedViews = computed(() => tagsViewStore.visitedViews)

const isActive = (currentRoute: VisitedViews) =>
  currentRoute.name === route.name ||
  currentRoute.meta.title === route.meta.title

const isAffix = (tag: { meta: { affix: boolean } }) =>
  tag.meta && tag.meta.affix

const filterAffixTags = (routes: RouteRecordRaw[]) => {
  let tags: Array<VisitedViews> = []
  routes.forEach((r: RouteRecordRaw) => {
    if (r.meta && r.meta.affix) {
      tags.push({
        fullPath: r.path,
        path: r.path,
        name: r.name as string,
        meta: { ...r.meta } as {
          title: string
          affix: boolean
          noCache: boolean
        },
      })
    }

    if (r.children) {
      const tempTags = filterAffixTags(r.children)
      if (tempTags.length >= 1) {
        tags = [...tags, ...tempTags]
      }
    }
  })
  return tags
}

const initTags = () => {
  affixTags.value = filterAffixTags(routes)
  affixTags.value.forEach((tag: VisitedViews) =>
    tag.meta.title ? tagsViewStore.addVisitedView(tag) : undefined,
  )
}

const addTags = () => {
  const { meta } = route
  if (meta.title && !meta.except) tagsViewStore.addView(route)
  return false
}

const moveToCurrentTag = () => {
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
}

const toLastView = (visitedViews: VisitedViews[], view: VisitedViews) => {
  const latestView = visitedViews.slice(-1)[0]
  if (latestView) router.push(latestView.fullPath)
  else {
    // now the default is to redirect to the home page if there is no tags-view,
    // you can adjust it according to your needs.
    if (view.name === 'Dashboard') {
      // to reload home page
      router.replace({ path: '/redirect' + view.fullPath })
    } else {
      router.push('/')
    }
  }
}

const closeSelectedTag = (view: VisitedViews) => {
  tagsViewStore.delView(view).then(({ visitedViews }: any) => {
    if (isActive(view)) toLastView(visitedViews, view)
  })
}

const closeMenu = () => {
  visible.value = false
}

watch(route, () => {
  addTags()
  moveToCurrentTag()
})

watch(visible, value => {
  if (value) {
    document.body.addEventListener('click', closeMenu)
  } else {
    document.body.removeEventListener('click', closeMenu)
  }
})

onMounted(() => {
  initTags()
  addTags()
})
</script>

<template>
  <v-sheet max-width="100%" class="my-1" :class="{ dark }">
    <v-slide-group show-arrows>
      <v-slide-group-item
        v-for="tag in visitedViews"
        :key="tag.path"
        ref="scrollPane"
        class="tags-view-item"
        @click.middle="!isAffix(tag) ? closeSelectedTag(tag) : ''"
      >
        <v-btn
          ref="currentTag"
          class="mx-1 my-0 text-body"
          :class="{ darkBtn: dark }"
          style="text-decoration: none"
          size="small"
          :border="true"
          :rounded="0"
          :color="isActive(tag) ? 'success' : btnColor"
          :to="{ name: tag.name, query: tag.query, fullPath: tag.fullPath }"
        >
          <v-icon
            v-if="isActive(tag)"
            icon="mdi-circle"
            size="x-small"
            class="mr-2"
          />
          {{ tag.meta.title }}
          <v-icon
            v-if="!isAffix(tag)"
            icon="mdi-close"
            size="x-small"
            class="pa-2 ml-1 close"
            @click.prevent.stop="closeSelectedTag(tag)"
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
