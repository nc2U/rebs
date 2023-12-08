<script lang="ts" setup="">
import { type PropType, ref } from 'vue'
import type { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

defineProps({
  noticeList: { type: Array as PropType<Post[]>, default: () => [] },
  postList: { type: Array as PropType<Post[]>, default: () => [] },
})

const msg = ref('공지 사항')
const items = ref([1, 2, 3, 4, 5, 6, 7, 8])
</script>

<template>
  <CRow>
    <CCol md="12">
      <v-card class="mx-auto mb-4">
        <v-table>
          <thead>
            <tr class="bg-secondary">
              <th class="text-left" colspan="2">
                <v-btn variant="text" icon="mdi-menu" />
                <span class="text-capitalize">{{ msg }}</span>
              </th>
              <th class="text-right">
                <router-link :to="{ name: '공지 사항' }">더보기</router-link>
                <v-icon icon="mdi-chevron-right" />
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in noticeList" :key="item.pk ?? 0">
              <td>
                <v-badge color="primary" content=" 공지 " offset-x="-10" offset-y="-7" />
              </td>
              <td>{{ cutString(item.title, 32) }}</td>
              <td class="text-right">{{ timeFormat(item.created ?? '') }}</td>
            </tr>
            <tr v-for="item in postList" :key="item.pk ?? 0">
              <td>{{ item.pk ?? 0 }}</td>
              <td>{{ cutString(item.title, 32) }}</td>
              <td class="text-right">{{ timeFormat(item.created ?? '') }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-card>
    </CCol>
  </CRow>
</template>
