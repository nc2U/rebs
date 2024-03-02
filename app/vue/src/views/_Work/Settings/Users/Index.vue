<script setup lang="ts">
import { computed, inject, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_Work/_menu/headermixin3'
import { useAccount } from '@/store/pinia/account'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import NoData from '@/views/_Work/components/NoData.vue'
import SearchList from '@/views/_Work/components/SearchList.vue'
import UserTable from '@/views/_Work/Settings/Users/components/UserTable.vue'

const cBody = ref()
const sideNavCAll = () => cBody.value.toggle()

const superAuth = inject('superAuth', false)

const accStore = useAccount()
const userList = computed(() => accStore.usersList)

onBeforeMount(() => accStore.fetchUsersList())
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <CRow class="py-2">
        <CCol>
          <h5>{{ $route.name }}</h5>
        </CCol>

        <CCol v-if="superAuth" class="text-right">
          <span class="mr-2">
            <v-icon icon="mdi-plus-circle" color="success" size="sm" />
            <router-link to="" class="ml-1">새 사용자</router-link>
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

    <template v-slot:aside></template>
  </ContentBody>
</template>
