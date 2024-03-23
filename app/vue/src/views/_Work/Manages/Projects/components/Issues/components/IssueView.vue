<script lang="ts" setup="">
import type { PropType } from 'vue'
import type { Issue } from '@/store/types/work'

defineProps({ issue: { type: Object as PropType<Issue>, default: undefined } })
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>
        <span>{{ issue?.tracker }} #{{ issue?.pk }}</span>
        <CBadge color="primary" variant="outline" class="ml-2">진행중</CBadge>
      </h5>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-pencil" color="amber" size="sm" />
        <router-link to="" class="ml-1">편집</router-link>
      </span>

      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-timer-edit-outline" color="grey" size="sm" />
        <router-link to="" class="ml-1">작업시간 기록</router-link>
      </span>

      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-star" color="amber" size="sm" />
        <router-link to="" class="ml-1">관심끄기</router-link>
      </span>

      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
        <v-icon icon="mdi-content-copy" color="grey" size="sm" />
        <router-link to="" class="ml-1">복사</router-link>
      </span>

      <span>
        <CDropdown color="secondary" variant="input-group" placement="bottom-end">
          <CDropdownToggle
            :caret="false"
            color="light"
            variant="ghost"
            size="sm"
            shape="rounded-pill"
          >
            <v-icon icon="mdi-dots-horizontal" class="pointer" color="grey-darken-1" />
            <v-tooltip activator="parent" location="top">Actions</v-tooltip>
          </CDropdownToggle>
          <CDropdownMenu>
            <CDropdownItem>
              <router-link to="">
                <v-icon icon="mdi-link-plus" color="grey" size="sm" />
                링크 복사
              </router-link>
            </CDropdownItem>
            <CDropdownItem>
              <router-link to="">
                <v-icon icon="mdi-trash-can-outline" color="grey" size="sm" />
                업무 삭제
              </router-link>
            </CDropdownItem>
          </CDropdownMenu>
        </CDropdown>
      </span>
    </CCol>
  </CRow>

  <CCard color="yellow-lighten-5 mb-3">
    <CCardBody>
      <span class="sub-title">권한별 프로젝트 목록 보기</span>
      <p class="mt-1">
        <router-link to="">austin2 kho</router-link>
        이(가)
        <router-link to="">23분</router-link>
        전에 추가함.
        <router-link to="">22분</router-link>
        전에 수정됨.
      </p>
      <CRow>
        <CCol>상태 :</CCol>
        <CCol>{{ issue?.status }}</CCol>
        <CCol>시작일:</CCol>
        <CCol>{{ issue?.start_date }}</CCol>
      </CRow>
      <CRow>
        <CCol>우선순위 :</CCol>
        <CCol>{{ issue?.priority }}</CCol>
        <CCol>완료일:</CCol>
        <CCol>{{ issue?.due_date }}</CCol>
      </CRow>

      <CRow>
        <CCol>담당자 :</CCol>
        <CCol>
          <router-link
            :to="{ name: '사용자 - 보기', params: { userId: issue?.assigned_to?.pk ?? 0 } }"
          >
            {{ issue?.assigned_to?.username }}
          </router-link>
        </CCol>
        <CCol>진척도:</CCol>
        <CCol>{{ issue?.done_ratio }}%</CCol>
      </CRow>

      <CRow>
        <CCol></CCol>
        <CCol></CCol>
        <CCol>추정시간:</CCol>
        <CCol>{{ issue?.estimated_hours }}</CCol>
      </CRow>

      <v-divider />

      <CRow class="mb-3">
        <CCol>설명</CCol>
        <CCol class="text-right">
          <v-icon icon="mdi-comment-text-outline" size="sm" color="info" class="mr-2" />
          <router-link to="">댓글달기</router-link>
        </CCol>
      </CRow>

      <CRow>
        <CCol>
          {{ issue?.description }}
        </CCol>
      </CRow>

      <v-divider />

      <CRow>
        <CCol>하위 일감</CCol>
        <CCol class="text-right">
          <router-link to="">추가</router-link>
        </CCol>
      </CRow>

      <v-divider />

      <CRow>
        <CCol>연결된 일감</CCol>
        <CCol class="text-right">
          <router-link to="">추가</router-link>
        </CCol>
      </CRow>
    </CCardBody>
  </CCard>

  <CNav variant="tabs">
    <CNavItem>
      <CNavLink>이력</CNavLink>
    </CNavItem>
    <CNavItem>
      <CNavLink>댓글</CNavLink>
    </CNavItem>
    <CNavItem>
      <CNavLink>항목 변경이력</CNavLink>
    </CNavItem>
  </CNav>
</template>

<style lang="scss" scoped>
.sub-title {
  font-size: 1.1em;
  font-weight: bold;
  color: #0f192a;
}
</style>
