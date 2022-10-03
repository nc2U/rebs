<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Editor from '@toast-ui/editor'
import '@toast-ui/editor/dist/toastui-editor.css'

defineProps({
  modelValue: {
    type: String,
    required: false,
    default: '',
  },
})
const emit = defineEmits(['update:modelValue'])

const editor = ref()

onMounted(() => {
  const e: Editor = new Editor({
    el: editor.value,
    height: '380px',
    initialEditType: 'wysiwyg',
    previewStyle: 'vertical',
    events: {
      change: () => emit('update:modelValue', e.getMarkdown()),
    },
  })
})
</script>

<template>
  <div>
    <div ref="editor" class="text-body" />
  </div>
</template>

<style lang="scss">
.dark-theme {
  .toastui-editor-defaultUI-toolbar {
    background: #24252f;
  }

  .toastui-editor-defaultUI-toolbar button:hover {
    background-color: #353641;
  }

  .toastui-editor-popup {
    background: #24252f;
  }

  .toastui-editor-popup li:hover {
    background: #353641;
  }

  .toastui-editor-contents {
    background-color: #353641;
    //color: #ffffff !important;
  }

  .toastui-editor-mode-switch {
    background-color: #30313e;

    .active {
      background-color: #353641 !important;
      color: #ffffff;
    }

    .tab-item {
      background-color: #24252f !important;
    }
  }
}
</style>
