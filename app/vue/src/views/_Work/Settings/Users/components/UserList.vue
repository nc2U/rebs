<script lang="ts" setup>
import { inject, type PropType } from 'vue'
import NoData from '@/views/_Work/components/NoData.vue'
import SearchList from '@/views/_Work/components/SearchList.vue'
import UserTable from '@/views/_Work/Settings/Users/components/UserTable.vue'
import type { User } from '@/store/types/accounts'

defineProps({
  userList: { type: Array as PropType<User[]>, default: () => [] },
})

const superAuth = inject('superAuth', false)
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>{{ $route.name }}</h5>
    </CCol>

    <CCol v-if="superAuth" class="text-right">
      <span class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '사용자 - 생성' }" class="ml-1">새 사용자</router-link>
      </span>

      <!--          <span>-->
      <!--            <CDropdown color="secondary" variant="input-group" placement="bottom-end">-->
      <!--              <CDropdownToggle-->
      <!--                :caret="false"-->
      <!--                color="light"-->
      <!--                variant="ghost"-->
      <!--                size="sm"-->
      <!--                shape="rounded-pill"-->
      <!--              >-->
      <!--                <v-icon icon="mdi-dots-horizontal" class="pointer" color="grey-darken-1" />-->
      <!--                <v-tooltip activator="parent" location="top">Actions</v-tooltip>-->
      <!--              </CDropdownToggle>-->
      <!--              <CDropdownMenu>-->
      <!--                <CDropdownItem>-->
      <!--                  <router-link to="">-->
      <!--                    <v-icon icon="mdi-file-document-arrow-right" color="success" size="sm" />-->
      <!--                    가져오기-->
      <!--                  </router-link>-->
      <!--                </CDropdownItem>-->
      <!--              </CDropdownMenu>-->
      <!--            </CDropdown>-->
      <!--          </span>-->
    </CCol>
  </CRow>

  <SearchList />

  <NoData v-if="!userList.length" />

  <CRow v-else>
    <CCol>
      <UserTable :user-list="userList" />
    </CCol>
  </CRow>
</template>
