<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import Datepicker from '@vuepic/vue-datepicker'

const store = useStore()
const isDark = computed(() => store.state.theme === 'dark')

const options = ref({ format: 'yyyy-MM-dd' })
</script>

<template>
  <Datepicker
    locale="ko"
    auto-apply
    text-input
    :text-input-options="options"
    :dark="isDark"
    position="left"
    :teleport="true"
    close-on-scroll
    format="yyyy-MM-dd"
    model-type="format"
    placeholder="날짜선택"
    allow-prevent-default
    :enable-time-picker="false"
    input-class-name="form-control"
  />
</template>
