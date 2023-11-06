<script lang="ts" setup="">
import { ref, computed, watch, onBeforeMount } from 'vue'
import { useStore } from '@/store'
import { useRebs } from '@/store/pinia/rebs'

const store = useStore()
const isDark = computed(() => store.theme === 'dark')

const bgColor = computed(() => (isDark.value ? 'success' : 'indigo-lighten-5'))

const defaults = ref({
  global: {
    elevation: 5,
  },
  VCard: {
    color: bgColor.value,
  },
})

watch(isDark, nVal => {
  defaults.value.VCard.color = nVal ? 'success' : 'indigo-lighten-5'
})

const rebsStore = useRebs()
const wiseWord = computed(() => rebsStore.wiseWord)
const wiseWordsCount = computed(() => rebsStore.wiseWordsCount)

const fetchWiseWordsList = () => rebsStore.fetchWiseWordsList()
const fetchWiseWord = (pk: number) => rebsStore.fetchWiseWord(pk)

const getPk = (max: number) => Math.floor(Math.random() * max)

onBeforeMount(() => {
  fetchWiseWordsList().then(() => {
    fetchWiseWord(getPk(wiseWordsCount.value))
    setInterval(() => fetchWiseWord(getPk(wiseWordsCount.value)), 90000)
  })
})
</script>

<template>
  <v-defaults-provider :defaults="defaults">
    <v-card
      :title="wiseWord?.saying_ko ?? ''"
      :subtitle="`${wiseWord?.saying_en ?? ''} - ${wiseWord?.spoked_by ?? ''}`"
      class="mb-4"
    />
  </v-defaults-provider>
</template>
