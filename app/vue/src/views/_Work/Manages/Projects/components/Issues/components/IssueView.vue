<script lang="ts" setup="">
import { ref, type PropType } from 'vue'
import type { Issue } from '@/store/types/work'

defineProps({ issue: { type: Object as PropType<Issue>, default: null } })

const tabPaneActiveKey = ref(1)
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

  <CNav variant="tabs" role="tablist" compact>
    <CNavItem>
      <CNavLink
        href="javascript:void(0);"
        :active="tabPaneActiveKey === 1"
        @click="
          () => {
            tabPaneActiveKey = 1
          }
        "
      >
        이력
      </CNavLink>
    </CNavItem>
    <CNavItem v-if="false">
      <CNavLink
        href="javascript:void(0);"
        :active="tabPaneActiveKey === 2"
        @click="
          () => {
            tabPaneActiveKey = 2
          }
        "
      >
        댓글
      </CNavLink>
    </CNavItem>
    <CNavItem>
      <CNavLink
        href="javascript:void(0);"
        :active="tabPaneActiveKey === 3"
        @click="
          () => {
            tabPaneActiveKey = 3
          }
        "
      >
        항목 변경이력
      </CNavLink>
    </CNavItem>
  </CNav>

  <CTabContent class="pt-3">
    <CTabPane role="tabpanel" aria-labelledby="home-tab" :visible="tabPaneActiveKey === 1">
      Raw denim you probably haven't heard of them jean shorts Austin. Nesciunt tofu stumptown
      aliqua, retro synth master cleanse. Mustache cliche tempor, williamsburg carles vegan
      helvetica. Reprehenderit butcher retro keffiyeh dreamcatcher synth. Cosby sweater eu banh mi,
      qui irure terry richardson ex squid. Aliquip placeat salvia cillum iphone. Seitan aliquip quis
      cardigan american apparel, butcher voluptate nisi qui.
    </CTabPane>
    <CTabPane role="tabpanel" aria-labelledby="profile-tab" :visible="tabPaneActiveKey === 2">
      Food truck fixie locavore, accusamus mcsweeney's marfa nulla single-origin coffee squid.
      Exercitation +1 labore velit, blog sartorial PBR leggings next level wes anderson artisan four
      loko farm-to-table craft beer twee. Qui photo booth letterpress, commodo enim craft beer
      mlkshk aliquip jean shorts ullamco ad vinyl cillum PBR. Homo nostrud organic, assumenda labore
      aesthetic magna delectus mollit. Keytar helvetica VHS salvia yr, vero magna velit sapiente
      labore stumptown. Vegan fanny pack odio cillum wes anderson 8-bit, sustainable jean shorts
      beard ut DIY ethical culpa terry richardson biodiesel. Art party scenester stumptown, tumblr
      butcher vero sint qui sapiente accusamus tattooed echo park.
    </CTabPane>
    <CTabPane role="tabpanel" aria-labelledby="contact-tab" :visible="tabPaneActiveKey === 3">
      Etsy mixtape wayfarers, ethical wes anderson tofu before they sold out mcsweeney's organic
      lomo retro fanny pack lo-fi farm-to-table readymade. Messenger bag gentrify pitchfork tattooed
      craft beer, iphone skateboard locavore carles etsy salvia banksy hoodie helvetica. DIY synth
      PBR banksy irony. Leggings gentrify squid 8-bit cred pitchfork. Williamsburg banh mi whatever
      gluten-free, carles pitchfork biodiesel fixie etsy retro mlkshk vice blog. Scenester cred you
      probably haven't heard of them, vinyl craft beer blog stumptown. Pitchfork sustainable tofu
      synth chambray yr.
    </CTabPane>
  </CTabContent>
</template>

<style lang="scss" scoped>
.sub-title {
  font-size: 1.1em;
  font-weight: bold;
  color: #0f192a;
}
</style>
