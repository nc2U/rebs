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
  <CRow>
    <CCol :xxl="9">
      <CCard class="mb-4">
        <CCardBody>
          <v-carousel
            cycle
            height="400"
            hide-delimiter-background
            show-arrows="hover"
          >
            <v-carousel-item
              v-for="(img, i) in imgSrc"
              :key="i"
              :src="img"
              cover
            />
          </v-carousel>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
</template>
