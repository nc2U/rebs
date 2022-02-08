<template>
  <CRow>
    <CCol :md="12">
      <CCard class="mb-4">
        <CCardHeader>
          <CIcon name="cil-justify-center" />
          <strong> Bootstrap Carousel</strong> <small class="text-muted">Songdo-Central Xi</small>
        </CCardHeader>
        <CCardBody>
          <CCarousel controls indicators>
            <CCarouselItem>
              <img
                class="d-block w-100"
                src="https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/001.png"
                alt="slide 1"
              />
              <CCarouselCaption class="d-none d-md-block">
                <h5>1st slide label</h5>
                <p>
                  Some representative placeholder content for the 1st slide.
                </p>
              </CCarouselCaption>
            </CCarouselItem>
            <CCarouselItem>
              <img
                class="d-block w-100"
                src="https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/002.png"
                alt="slide 2"
              />
              <CCarouselCaption class="d-none d-md-block">
                <h5>2nd slide label</h5>
                <p>
                  Some representative placeholder content for the 2nd slide.
                </p>
              </CCarouselCaption>
            </CCarouselItem>
            <CCarouselItem>
              <img
                class="d-block w-100"
                src="https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/003.png"
                alt="slide 3"
              />
              <CCarouselCaption class="d-none d-md-block">
                <h5>3rd slide label</h5>
                <p>
                  Some representative placeholder content for the 3rd slide.
                </p>
              </CCarouselCaption>
            </CCarouselItem>
            <CCarouselItem>
              <img
                class="d-block w-100"
                src="https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/004.png"
                alt="slide 4"
              />
              <CCarouselCaption class="d-none d-md-block">
                <h5>4th slide label</h5>
                <p>
                  Some representative placeholder content for the 4th slide.
                </p>
              </CCarouselCaption>
            </CCarouselItem>
            <CCarouselItem>
              <img
                class="d-block w-100"
                src="https://brdnc-buket.s3.ap-northeast-2.amazonaws.com/image/carousel/005.png"
                alt="slide 5"
              />
              <CCarouselCaption class="d-none d-md-block">
                <h5>5th slide label</h5>
                <p>
                  Some representative placeholder content for the 5th slide.
                </p>
              </CCarouselCaption>
            </CCarouselItem>
          </CCarousel>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MainCarousel',
})
</script>
