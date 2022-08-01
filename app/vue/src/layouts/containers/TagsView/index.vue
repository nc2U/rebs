<script lang="ts" setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { VisitedViews } from '@/store/modules/tagsView/state'
import routes from '@/router/routes'
// const routes = computed(() => store.state.permission.routes)

const visible = ref(false)
const top = ref(0)
const left = ref(0)
const selectedTag = reactive({})
let affixTags: any[] = reactive([])
const tag = ref()
const scrollPane = ref()

const store = useStore()
const dark = computed(() => store.state.theme === 'dark')
const btnColor = computed(() =>
  store.state.theme === 'dark' ? 'blue-grey' : '',
)

const route = useRoute()
const router = useRouter()

const visitedViews = computed(() => store.state.tagsView.visitedViews)

const isActive = (currentRoute: any) => currentRoute.path === route.path

const isAffix = (tag: any) => tag.meta && tag.meta.affix

const filterAffixTags = (routes: any[]) => {
  let tags: Array<VisitedViews> = []
  routes.forEach((r: any) => {
    if (r.meta && r.meta.affix) {
      if (r.name !== route.name) {
        tags.push({
          path: r.path,
          name: r.name,
          meta: { ...r.meta },
        })
      }
      console.log(r)
      console.log('-----------------')
      console.log(route.name)
    }
    if (r.children) {
      const tempTags = filterAffixTags(r.children)
      if (tempTags.length >= 1) {
        tags = [...tags, ...tempTags]
      }
    }
  })
  return tags.filter((v, i) => tags.indexOf(v) == i)
}

const initTags = () => {
  affixTags = filterAffixTags(routes)
  affixTags.forEach(tag =>
    tag.name ? store.dispatch('tagsView/addVisitedView', tag) : undefined,
  )
}

const addTags = () => {
  const { name } = route
  if (name) {
    store.dispatch('tagsView/addView', route)
  }
  return false
}

const moveToCurrentTag = () => {
  const tags = tag.value
  nextTick(() => {
    for (const tag of tags) {
      if (tag.to.path === route.path) {
        scrollPane.value.moveToTarget(tag)
        // when query is different then update
        if (tag.to.fullPath !== route.fullPath) {
          store.dispatch('tagsView/updateVisitedView', route)
        }
        break
      }
    }
  })
}

const refreshSelectedTag = (view: any) => {
  store.dispatch('tagsView/delCachedView', view).then(() => {
    const { fullPath } = view
    nextTick(() => {
      router.replace({
        path: '/redirect' + fullPath,
      })
    })
  })
}

const toLastView = (visitedViews: any, view: any) => {
  const latestView = visitedViews.slice(-1)[0]
  if (latestView) {
    router.push(latestView.fullPath)
  } else {
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

const closeSelectedTag = (view: any) => {
  store.dispatch('tagsView/delView', view).then(({ visitedViews }) => {
    if (isActive(view)) {
      toLastView(visitedViews, view)
    }
  })
}

const closeOthersTags = () => {
  router.push(selectedTag)
  store.dispatch('tagsView/delOthersViews', selectedTag).then(() => {
    moveToCurrentTag()
  })
}

const closeAllTags = (view: any) => {
  store.dispatch('tagsView/delAllViews').then(({ visitedViews }) => {
    if (affixTags.some(tag => tag.path === view.path)) {
      return
    }
    toLastView(visitedViews, view)
  })
}

const closeMenu = () => {
  visible.value = false
}

const handleScroll = () => {
  closeMenu()
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
  <v-sheet max-width="100%" class="my-2" :class="{ dark }">
    <v-slide-group ref="scrollPane" show-arrows>
      <v-slide-group-item
        v-for="tag in visitedViews"
        ref="tag"
        :key="tag.path"
        tag="span"
        class="tags-view-item"
        @click.middle="!isAffix(tag) ? closeSelectedTag(tag) : ''"
      >
        <v-btn
          class="mx-1 my-0 text-body"
          :class="{ darkBtn: dark }"
          size="x-small"
          :border="true"
          :rounded="0"
          :color="isActive(tag) ? 'success' : btnColor"
          :to="{ path: tag.path, query: tag.query, fullPath: tag.fullPath }"
        >
          <v-icon
            v-if="isActive(tag)"
            icon="mdi-circle"
            size="x-small"
            class="mr-2"
          />
          {{ tag.title }}
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
  background: #181924;
}
</style>
