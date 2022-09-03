<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Datepicker from '@vuepic/vue-datepicker'
import { dateFormat } from '@/utils/baseMixins'
import { maska as vMaska } from 'maska'

const store = useStore()

const textInputOptions = computed(() => ({
  enterSubmit: true,
  tabSubmit: true,
  openMenu: true,
  format: 'yyyy-MM-dd',
}))

const isDark = computed(() => store.state.theme === 'dark')
</script>

<template>
  <Datepicker
    v-maska="'####-##-##'"
    name="date-picker"
    text-input
    auto-apply
    :format="dateFormat"
    position="left"
    :text-input-options="textInputOptions"
    input-class-name="form-control"
    :enable-time-picker="false"
    teleport="#app"
    :dark="isDark"
    locale="ko"
    required
  />
</template>
