<script setup lang="ts">
import { useStore } from 'vuex'
import Editor from '@tinymce/tinymce-vue'
import { computed } from 'vue'

const store = useStore()
const isDark = computed(() => store.state.theme)
const editorSkin = computed(() =>
  isDark.value === 'dark' ? 'oxide-dark' : 'oxide',
)
</script>

<template>
  <Editor
    api-key="11ntkikesp2cxo74r2lzk7b76i5oajmeixas0of64z4ugj7k"
    :init="{
      // selector: 'textarea', // change this value according to your HTML
      language: 'ko_KR',
      plugins:
        'print preview powerpaste casechange importcss tinydrive searchreplace autolink autosave save directionality advcode visualblocks visualchars fullscreen image link media mediaembed template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists checklist wordcount tinymcespellchecker a11ychecker imagetools textpattern noneditable help formatpainter permanentpen pageembed charmap mentions quickbars linkchecker emoticons advtable export',
      mobile: {
        plugins:
          'print preview powerpaste casechange importcss tinydrive searchreplace autolink autosave save directionality advcode visualblocks visualchars fullscreen image link media mediaembed template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists checklist wordcount tinymcespellchecker a11ychecker textpattern noneditable help formatpainter pageembed charmap mentions quickbars linkchecker emoticons advtable',
      },
      menubar: false,
      toolbar:
        'undo redo | bold italic underline strikethrough | formatselect fontsizeselect | forecolor backcolor | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist checklist | pagebreak | image media codesample | fullscreen  preview save print | charmap emoticons',
      skin: editorSkin,
      content_css: isDark,
      statusbar: false,
    }"
  />
</template>
