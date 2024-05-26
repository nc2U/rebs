<script lang="ts" setup>
import { type PropType } from 'vue'
import type { Version } from '@/store/types/work'

defineProps({ versionList: { type: Array as PropType<Version[]>, default: () => [] } })

const boxClass = ['primary-box', 'danger-box', 'success-box']
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>로드맵</h5>
    </CCol>

    <CCol class="text-right">
      <span class="mr-2 form-text">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '(로드맵) - 추가' }" class="ml-1"> 새 버전 </router-link>
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
            <CDropdownItem
              v-if="$route.params.projId"
              class="form-text"
              @click="$router.push({ name: '(설정)', query: { menu: '버전' } })"
            >
              <router-link to="">
                <v-icon icon="mdi-cog" color="grey" size="sm" class="mr-2" />
                설정
              </router-link>
            </CDropdownItem>
          </CDropdownMenu>
        </CDropdown>
      </span>
    </CCol>
  </CRow>

  <CRow v-for="ver in versionList" :key="ver.pk">
    <CCol>
      <CRow>
        <CCol>
          <v-icon icon="mdi-star-box-multiple" color="amber" class="mr-2" />
          <span class="mr-2 bold" style="font-size: large">
            <router-link :to="{ name: '(로드맵) - 보기', params: { verId: ver.pk } }">
              {{ ver.name }}
            </router-link>
          </span>

          <span :class="boxClass[Number(ver.status) - 1]">
            {{ ver.status_desc }}
          </span>
        </CCol>
        <CCol class="text-right">
          <v-icon icon="mdi-pencil" color="amber" size="18" />
        </CCol>
      </CRow>
    </CCol>
  </CRow>
</template>
