<script lang="ts" setup="">
import { ref } from 'vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'

const msg = ref('My page!')
</script>

<template>
  <ContentBody>
    <CNav variant="tabs" class="m-5">
      <CNavItem>
        <CNavLink :active="true">내 정보</CNavLink>
      </CNavItem>
      <CNavItem>
        <CNavLink>나의 작성글</CNavLink>
      </CNavItem>
      <CNavItem>
        <CNavLink>좋아요 표시글</CNavLink>
      </CNavItem>
      <CNavItem>
        <CNavLink>스크랩</CNavLink>
      </CNavItem>
      <CNavItem>
        <CNavLink>로그인기록</CNavLink>
      </CNavItem>
      <CNavItem>
        <CNavLink>정보수정</CNavLink>
      </CNavItem>
      <CNavItem>
        <CNavLink>탈퇴하기</CNavLink>
      </CNavItem>
    </CNav>
  </ContentBody>
</template>
