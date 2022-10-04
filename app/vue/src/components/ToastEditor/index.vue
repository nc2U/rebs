<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useStore } from 'vuex'
import Editor from '@toast-ui/editor'
import colorSyntax from '@toast-ui/editor-plugin-color-syntax'
import codeSyntaxHighlight from '@toast-ui/editor-plugin-code-syntax-highlight'
import tableMergedCell from '@toast-ui/editor-plugin-table-merged-cell'
import chart from '@toast-ui/editor-plugin-chart'
import '@toast-ui/editor/dist/toastui-editor.css'
import '@toast-ui/editor/dist/theme/toastui-editor-dark.css'
import 'tui-color-picker/dist/tui-color-picker.css'
import '@toast-ui/editor-plugin-color-syntax/dist/toastui-editor-plugin-color-syntax.css'
import 'prismjs/themes/prism.css'
import '@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight.css'
import '@toast-ui/editor-plugin-table-merged-cell/dist/toastui-editor-plugin-table-merged-cell.css'
import '@toast-ui/chart/dist/toastui-chart.css'

const props = defineProps({
  modelValue: {
    type: String,
    required: false,
    default: '',
  },
})
const emit = defineEmits(['update:modelValue'])

const editor = ref()

const store = useStore()
const theme = computed(() => store.state.theme)

const chartOptions = {
  minWidth: 100,
  maxWidth: 600,
  minHeight: 100,
  maxHeight: 300,
}

const createEditor = () => {
  const e: Editor = new Editor({
    el: editor.value,
    height: '380px',
    initialEditType: 'wysiwyg',
    initialValue: props.modelValue || ' ',
    previewStyle: 'vertical',
    events: {
      change: () => emit('update:modelValue', e.getHTML()),
    },
    theme: theme.value,
    plugins: [
      colorSyntax,
      codeSyntaxHighlight,
      tableMergedCell,
      [chart, chartOptions],
    ],
  })
  return e
}

watch(theme, () => createEditor())
onMounted(() => {
  createEditor()
  setTimeout(() => createEditor(), 600)
})
</script>

<template>
  <div>
    <div ref="editor" />
  </div>
</template>

<style lang="scss">
.toastui-editor-contents {
  font-size: 1em;
}

.toastui-editor-dark .toastui-editor-defaultUI-toolbar {
  background-color: #1c1d2a;
  border-bottom-color: #303238;
}

.toastui-editor-dark .toastui-editor-md-container,
.toastui-editor-dark .toastui-editor-ww-container {
  background-color: #2f303a;
}

.toastui-editor-dark .toastui-editor-main .toastui-editor-md-splitter {
  background-color: #393b42;
}

.toastui-editor-dark .toastui-editor-mode-switch {
  border-top-color: #393b42;
  background-color: #24252f;
}

.toastui-editor-dark .toastui-editor-mode-switch .tab-item.active {
  border-top-color: #2f303a;
  background-color: #2f303a;
}
</style>
