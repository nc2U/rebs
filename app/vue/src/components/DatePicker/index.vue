<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { dateFormat } from '@/utils/baseMixins'
import { maska as vMaska } from 'maska'
import Datepicker from '@vuepic/vue-datepicker'

const store = useStore()

const textInputOptions = ref({
  enterSubmit: true,
  tabSubmit: true,
  openMenu: true,
  format: 'yyyy-MM-dd',
})

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
  />
</template>
