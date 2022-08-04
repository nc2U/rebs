<script lang="ts" setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { VisitedViews } from '@/store/modules/tagsView/state'
import routes from '@/router/routes'

const store = useStore()
const route = useRoute()
const router = useRouter()

const visible = ref(false)
let affixTags: any[] = reactive([])

const currentTag = ref()
const scrollPane = ref()

const dark = computed(() => store.state.theme === 'dark')
const btnColor = computed(() =>
  store.state.theme === 'dark' ? 'blue-grey' : '',
)

const visitedViews = computed(() => store.state.tagsView.visitedViews)

const isActive = (currentRoute: any) => currentRoute.name === route.name

const isAffix = (tag: any) => tag.meta && tag.meta.affix

const filterAffixTags = (routes: any[]) => {
  let tags: Array<VisitedViews> = []
  routes.forEach((r: any) => {
    if (r.meta && r.meta.affix && r.name !== 'Login') {
      tags.push({
        fullPath: r.path,
        path: r.path,
        name: r.name,
        meta: { ...r.meta },
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
  const tags = currentTag.value
  nextTick(() => {
    for (const tag of tags) {
      if (tag.to.path === route.path) {
        // when query is different then update
        if (tag.to.fullPath !== route.fullPath) {
          store.dispatch('tagsView/updateVisitedView', route)
        }
        break
      }
    }
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
