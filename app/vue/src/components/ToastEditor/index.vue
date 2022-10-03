<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useStore } from 'vuex'
import Editor from '@toast-ui/editor'
import '@toast-ui/editor/dist/toastui-editor.css'
import '@toast-ui/editor/dist/theme/toastui-editor-dark.css'

defineProps({
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

watch(theme, () => {
  const e: Editor = new Editor({
    el: editor.value,
    height: '380px',
    initialEditType: 'wysiwyg',
    previewStyle: 'vertical',
    events: {
      change: () => emit('update:modelValue', e.getMarkdown()),
    },
    theme: theme.value,
  })
})

onMounted(() => {
  const e: Editor = new Editor({
    el: editor.value,
    height: '380px',
    initialEditType: 'wysiwyg',
    previewStyle: 'vertical',
    events: {
      change: () => emit('update:modelValue', e.getMarkdown()),
    },
    theme: theme.value,
  })
})
</script>

<template>
  <div>
    <div ref="editor" class="text-body" />
  </div>
</template>

<style lang="scss">
.toastui-editor-contents {
  font-size: 15px;
}

.toastui-editor-dark .toastui-editor-defaultUI-toolbar {
  background-color: #181924;
  border-bottom-color: #303238;
}

.dark-theme {
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
}
</style>
