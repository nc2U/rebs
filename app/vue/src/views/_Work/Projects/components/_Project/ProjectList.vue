<script lang="ts" setup="">
import { ref } from 'vue'

const projectList = ref([
  {
    pk: 1,
    name: '동춘1구역9블럭 지역주택조합',
    desc: '동춘1구역9블럭 지역주택조합 공동주택 신축사업',
    slug: 'dongchun',
  },
  {
    pk: 2,
    name: 'Redmine clone 프로젝트',
    desc: 'Redmine clone 및 최적화 프로젝트',
    slug: 'redmine-clone',
  },
])
</script>

<template>
  <CRow>
    <CCol class="my-3">
      <h5>프로젝트</h5>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 생성'" class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '프로젝트 - 생성' }" class="ml-1">새 프로젝트</router-link>
      </span>
      <span>
        <v-icon icon="mdi-cog" color="secondary" size="sm" />
        <router-link :to="{ name: '프로젝트 목록' }" class="ml-1">관리</router-link>
      </span>
    </CCol>
  </CRow>

  <CRow>
    <CCol v-for="proj in projectList" :key="proj.pk" sm="12" lg="6" xl="4" class="my-2">
      <CCard>
        <CCardBody class="card">
          <router-link :to="{ name: '(개요)', params: { projId: proj.slug } }">
            {{ proj.name }}
          </router-link>
          <p>{{ proj.desc }}</p>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
</template>

<style lang="scss" scoped>
h5 {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-weight: bold;
}

.card a {
  font-weight: bold;
  font-size: 1.1em;
  //color: #5889ce;
}

.card p {
  font-size: 0.9em;
}
</style>
