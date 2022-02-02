<template>
  <CFooter class="mt-4">
    <div>
      <a href="https://brdnc.co.kr" target="_blank">Rebs</a>
      <span class="ms-1"
        >&copy; {{ new Date().getFullYear() }} creativeLabs.</span
      >
    </div>
    <div class="ms-auto">
      <span class="me-1" target="_blank">Powered by</span>
      <a href="#">CoreUI for Vue</a>
    </div>
  </CFooter>
</template>

<script lang="ts">
export default {
  name: 'AppFooter',
}
</script>
