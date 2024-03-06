<script lang="ts" setup>
import { inject, onBeforeMount, type PropType } from 'vue'
import type { IssueProject } from '@/store/types/work'
import SearchList from '@/views/_Work/components/SearchList.vue'
import NoData from '@/views/_Work/components/NoData.vue'

defineProps({
  projectList: {
    type: Array as PropType<IssueProject[]>,
    default: () => [],
  },
})

const emit = defineEmits(['aside-visible'])

const superAuth = inject('superAuth', false)

onBeforeMount(() => emit('aside-visible', true))
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

  <SearchList />

  <NoData v-if="!projectList.length" />

  <CRow v-else>
    <CCol v-for="proj in projectList" :key="proj.pk" sm="12" lg="6" xl="4">
      <CCard class="my-2">
        <CCardBody class="project-set">
          <router-link :to="{ name: '(개요)', params: { projId: proj.slug } }">
            {{ proj.name }}
          </router-link>
          <p v-html="proj.description" />

          <!-- c1 -->
          <div v-if="!!proj.sub_projects?.length" class="child">
            <blockquote v-for="c1 in proj.sub_projects" :key="c1.pk">
              <router-link :to="{ name: '(개요)', params: { projId: c1.slug } }">
                {{ c1.name }}
              </router-link>
              <p v-html="c1.description" />

              <!-- c2 -->
              <div v-if="!!c1.sub_projects?.length" class="child">
                <blockquote v-for="c2 in c1.sub_projects" :key="c2.pk">
                  <router-link :to="{ name: '(개요)', params: { projId: c2.slug } }">
                    {{ c2.name }}
                  </router-link>
                  <p v-html="c2.description" />

                  <!-- c3 -->
                  <div v-if="!!c2.sub_projects?.length" class="child">
                    <blockquote v-for="c3 in c2.sub_projects" :key="c3.pk">
                      <router-link :to="{ name: '(개요)', params: { projId: c3.slug } }">
                        {{ c3.name }}
                      </router-link>
                      <p v-html="c3.description" />

                      <!-- c4 -->
                      <div v-if="!!c3.sub_projects?.length" class="child">
                        <blockquote v-for="c4 in c3.sub_projects" :key="c4.pk">
                          <router-link :to="{ name: '(개요)', params: { projId: c4.slug } }">
                            {{ c4.name }}
                          </router-link>
                          <p v-html="c4.description" />

                          <!-- c5 -->
                          <div v-if="!!c4.sub_projects?.length" class="child">
                            <blockquote v-for="c5 in c4.sub_projects" :key="c5.pk">
                              <router-link :to="{ name: '(개요)', params: { projId: c5.slug } }">
                                {{ c5.name }}
                              </router-link>
                              <p v-html="c5.description" />
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
.project-set {
  padding-bottom: 0;
}

.project-set a {
  font-weight: bold;
  font-size: 1.13em;
}

.project-set .child {
  a {
    font-size: 0.96em;
    font-weight: normal;
  }

  padding-left: 12px;
  border-left: 3px solid #ddd;
}
</style>