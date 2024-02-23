<script lang="ts" setup="">
import { ref } from 'vue'

const projectList = ref([
  {
    pk: 1,
    name: '동춘1구역9블럭 지역주택조합',
    desc: '동춘1구역9블럭 지역주택조합 공동주택 신축사업',
    slug: 'dongchun',
    child: [
      {
        pk: 3,
        name: '공급계약 95% 전환',
        desc: '도급계약 유효조건 (공급계약 95%) 달성하기',
        slug: 'cont-95',
        child: [
          {
            pk: 5,
            name: '그랜드 차일드 프로젝트 1111',
            desc: '-------------------',
            slug: 'cont-955',
            child: [],
          },
        ],
      },
      {
        pk: 4,
        name: '착공하기',
        desc: '도급계약 유효조건 (공급계약 95%) 달성하기',
        slug: 'cont-96',
        child: [],
      },
    ],
  },
  {
    pk: 2,
    name: 'Redmine clone 프로젝트',
    desc: 'Redmine clone 및 최적화 프로젝트',
    slug: 'redmine-clone',
    child: [],
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

          <span v-if="!!proj.child?.length" class="child pb-0">
            <blockquote v-for="child in proj.child" :key="child.pk" class="mb-0">
              <router-link :to="{ name: '(개요)', params: { projId: child.slug } }">
                {{ child.name }}
              </router-link>
              <p>{{ child.desc }}</p>

              <span v-if="!!child?.child?.length" class="child pb-0">
                <blockquote v-for="child1 in child.child" :key="child1.pk" class="mb-0">
                  <router-link :to="{ name: '(개요)', params: { projId: child1.slug } }">
                    {{ child1.name }}
                  </router-link>
                  <p>{{ child1.desc }}</p>

                  <span v-if="!!child1?.child?.length" class="child pb-0">
                    <blockquote v-for="child2 in child1.child" :key="child2.pk" class="mb-0">
                      <router-link :to="{ name: '(개요)', params: { projId: child2.slug } }">
                        {{ child2.name }}
                      </router-link>
                      <p>{{ child2.desc }}</p>

                      <span v-if="!!child2?.child?.length" class="child pb-0">
                        <blockquote v-for="child3 in child2.child" :key="child3.pk" class="mb-0">
                          <router-link :to="{ name: '(개요)', params: { projId: child3.slug } }">
                            {{ child3.name }}
                          </router-link>
                          <p>{{ child3.desc }}</p>
                        </blockquote>
                      </span>
                    </blockquote>
                  </span>
                </blockquote>
              </span>
            </blockquote>
          </span>
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
  font-size: 1.13em;
}

.card p {
  font-size: 0.89em;
}

.card .child {
  a {
    font-size: 0.96em;
    font-weight: normal;
  }
}

.card blockquote {
  padding-left: 12px;
  border-left: 3px solid #ddd;
}
</style>
