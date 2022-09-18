<script setup lang="ts">
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'

const editor = useEditor({
  content: '',
  extensions: [StarterKit],
  autofocus: true,
  editable: true,
  injectCSS: false,
})
</script>

<template>
  <EditorContent :editor="editor" class="form-control" />
</template>
