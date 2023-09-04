<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from '@/store'
import { vMaska } from 'maska'
import Datepicker from '@vuepic/vue-datepicker'

defineProps({
  placeholder: { type: String, default: '날짜선택' },
})

const store = useStore()
const isDark = computed(() => store.theme === 'dark')

const options = ref({ format: 'yyyy-MM-dd' })
</script>

<template>
  <Datepicker
    locale="ko"
    auto-apply
    text-input
    :dark="isDark"
    position="left"
    :teleport="true"
    format="yyyy-MM-dd"
    model-type="format"
    allow-prevent-default
    :enable-time-picker="false"
    :text-input-options="options"
  >
    <template #input-icon>
      <v-icon icon="mdi mdi-calendar-blank-outline" class="m-2" size="16" />
    </template>
    <template #dp-input="{ value }">
      <input
        v-maska
        data-maska="####-##-##"
        :value="value"
        class="form-control dp__input dp__input_icon_pad"
        aria-label="Datepicker input"
        autocomplete="off"
        :placeholder="placeholder"
      />
    </template>
  </Datepicker>
</template>
