<script lang="ts" setup="">
import { ref } from 'vue'

const msg = ref('공지 게시판')
const items = ref([1, 2, 3, 4, 5, 6, 7, 8])
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
                <span class="text-capitalize">{{ msg }}</span>
              </th>
              <th class="text-right">
                <router-link :to="{ name: '공지 게시판' }">더보기</router-link>
                <v-icon icon="mdi-chevron-right" />
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item">
              <td>{{ item }}</td>
              <td class="text-right">{{ '11-02' }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-card>
    </CCol>
  </CRow>
</template>
