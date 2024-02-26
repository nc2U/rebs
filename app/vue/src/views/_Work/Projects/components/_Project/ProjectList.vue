<script lang="ts" setup>
import { inject, type PropType } from 'vue'
import type { TaskProject } from '@/store/types/work'

defineProps({
  projectList: {
    type: Array as PropType<TaskProject[]>,
    default: () => [],
  },
})

const superAuth = inject('superAuth', false)
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>프로젝트</h5>
    </CCol>

    <CCol v-if="superAuth" class="text-right">
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

  <CRow v-if="!projectList.length">
    <CAlert color="warning" class="text-center"> 표시할 데이터가 없습니다.</CAlert>
  </CRow>

  <CRow v-else>
    <CCol v-for="proj in projectList" :key="proj.pk" sm="12" lg="6" xl="4">
      <CCard class="my-2">
        <CCardBody class="project-set">
          <router-link :to="{ name: '(개요)', params: { projId: proj.slug } }">
            {{ proj.name }}
          </router-link>
          <p v-html="proj.desc" />

          <!-- c1 -->
          <div v-if="!!proj.sub_projects?.length" class="child">
            <blockquote v-for="c1 in proj.sub_projects" :key="c1.pk">
              <router-link :to="{ name: '(개요)', params: { projId: c1.slug } }">
                {{ c1.name }}
              </router-link>
              <p v-html="c1.desc" />

              <!-- c2 -->
              <div v-if="!!c1.sub_projects?.length" class="child">
                <blockquote v-for="c2 in c1.sub_projects" :key="c2.pk">
                  <router-link :to="{ name: '(개요)', params: { projId: c2.slug } }">
                    {{ c2.name }}
                  </router-link>
                  <p v-html="c2.desc" />

                  <!-- c3 -->
                  <div v-if="!!c2.sub_projects?.length" class="child">
                    <blockquote v-for="c3 in c2.sub_projects" :key="c3.pk">
                      <router-link :to="{ name: '(개요)', params: { projId: c3.slug } }">
                        {{ c3.name }}
                      </router-link>
                      <p v-html="c3.desc" />

                      <!-- c4 -->
                      <div v-if="!!c3.sub_projects?.length" class="child">
                        <blockquote v-for="c4 in c3.sub_projects" :key="c4.pk">
                          <router-link :to="{ name: '(개요)', params: { projId: c4.slug } }">
                            {{ c4.name }}
                          </router-link>
                          <p v-html="c4.desc" />

                          <!-- c5 -->
                          <div v-if="!!c4.sub_projects?.length" class="child">
                            <blockquote v-for="c5 in c4.sub_projects" :key="c5.pk">
                              <router-link :to="{ name: '(개요)', params: { projId: c5.slug } }">
                                {{ c5.name }}
                              </router-link>
                              <p v-html="c5.desc" />
                            </blockquote>
                          </div>
                        </blockquote>
                      </div>
                    </blockquote>
                  </div>
                </blockquote>
              </div>
            </blockquote>
          </div>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
</template>

<style lang="scss" scoped>
.project-set a {
  font-weight: bold;
  font-size: 1.13em;
}

.project-set .child {
  a {
    font-size: 0.96em;
    font-weight: normal;
  }
}

.project-set .child {
  padding-left: 12px;
  border-left: 3px solid #ddd;
}
</style>
