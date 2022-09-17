<script setup lang="ts">
import ContentBody from '@/layouts/ContentBody/Index.vue'
</script>

<template>
  <ContentBody>
    <CCardBody class="blank-body text-center">
      <p class="code">404</p>
      <h1 class="title">PAGE NOT FOUND</h1>
      <div class="divider"></div>
      <blockquote class="quote">
        But if you don't change your direction, and if you keep looking, you may
        end up where you are heading.
      </blockquote>

      <v-btn
        color="info"
        variant="outlined"
        rounded="pill"
        @click="$router.go(-1)"
      >
        To previous
      </v-btn>

      <span class="horizontal-divider">|</span>

      <v-btn
        color="success"
        variant="outlined"
        rounded="pill"
        @click="$router.replace({ path: '/' })"
      >
        Take me home
      </v-btn>
    </CCardBody>
    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<style lang="scss" scoped>
.card-body {
  height: 650px;
  padding-top: 180px;

  p.code {
    line-height: 64px;
    font-size: 64px;
    font-weight: 600;
  }

  h1.title {
    letter-spacing: 2px;
    line-height: 20px;
    font-size: 20px;
    font-weight: 700;
  }

  .divider {
    margin: 24px auto 18px;
    width: 64px;
    height: 1px;
    background-color: #c6c6c6;
  }

  .quote {
    margin: 0 auto;
    max-width: 256px;
    font-size: 14px;
    font-weight: 500;
    color: #767676;
  }

  .horizontal-divider {
    display: inline-block;
    margin-top: 32px;
    margin-right: 10px;
    margin-left: 10px;
    color: #c6c6c6;
  }
}
</style>
