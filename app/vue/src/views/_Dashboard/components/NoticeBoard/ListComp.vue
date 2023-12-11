<script lang="ts" setup="">
import { type PropType } from 'vue'
import type { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

defineProps({
  mainViewName: { type: String, default: '공지 사항' },
  noticeList: { type: Array as PropType<Post[]>, default: () => [] },
  postList: { type: Array as PropType<Post[]>, default: () => [] },
})
</script>

<template>
  <CRow>
    <CCol md="12">
      <v-card class="mx-auto mb-4">
        <v-table>
          <thead>
            <tr class="bg-secondary">
              <th class="text-left">
                <v-btn variant="text" icon="mdi-menu" />
                <span class="text-capitalize">{{ mainViewName }}</span>
              </th>
              <th class="text-right">
                <router-link :to="{ name: mainViewName }">더보기</router-link>
                <v-icon icon="mdi-chevron-right" />
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in noticeList" :key="item.pk ?? 0">
              <td class="pl-5">
                <v-badge
                  v-if="item.is_notice"
                  color="primary"
                  content="!"
                  offset-x="20"
                  offset-y="-7"
                />
                <router-link :to="{ name: `${mainViewName} - 보기`, params: { postId: item.pk } }">
                  {{ cutString(item.title, 32) }}
                </router-link>
              </td>
              <td class="text-right pr-5">{{ timeFormat(item.created ?? '').substring(0, 10) }}</td>
            </tr>
            <template v-for="(item, i) in postList" :key="item.pk ?? 0">
              <tr v-if="(noticeList.length ?? 0) + i <= 7">
                <td class="pl-5">
                  <router-link
                    :to="{ name: `${mainViewName} - 보기`, params: { postId: item.pk } }"
                  >
                    {{ cutString(item.title, 32) }}
                  </router-link>
                </td>
                <td class="text-right pr-5">
                  {{ timeFormat(item.created ?? '').substring(0, 10) }}
                </td>
              </tr>
            </template>
          </tbody>
        </v-table>
      </v-card>
    </CCol>
  </CRow>
</template>
