<script lang="ts" setup>
const imgSrc = [
  'https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/001.png',
  'https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/002.png',
  'https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/003.png',
  'https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/004.png',
  'https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/005.png',
]
</script>
<template>
  <CCard class="mb-4" xxl="9">
    <CCardBody>
      <v-carousel
        cycle
        height="400"
        delimiter-icon="mdi-square"
        show-arrows="hover"
      >
        <v-carousel-item v-for="(img, i) in imgSrc" :key="i" :src="img" cover />
      </v-carousel>
    </CCardBody>
  </CCard>
</template>
