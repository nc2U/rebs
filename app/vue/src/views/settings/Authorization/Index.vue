<script lang="ts" setup>
// import { computed } from 'vue'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { useStore } from 'vuex'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'

const store = useStore()

// const company = computed(() => store.state.settings.company)
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="onSelectAdd"
  />
  <ContentBody></ContentBody>
</template>
