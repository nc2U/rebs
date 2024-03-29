<script lang="ts" setup>
import { computed, inject, onBeforeMount } from 'vue'
import { useWork } from '@/store/pinia/work'
import type { SimpleMember } from '@/store/types/work'

const emit = defineEmits(['aside-visible'])

const isDark = inject('isDark')

const workStore = useWork()
const iProject = computed(() => workStore.issueProject)

const allMembers = computed<SimpleMember[]>(() => workStore.issueProject?.all_members ?? [])

const computedMembers = computed(() => {
  const organizedData = {} as { [key: string]: Array<{ pk: number; username: string }> }

  allMembers.value.forEach(item => {
    // Iterate over the roles of each user
    item.roles.forEach(role => {
      // If the role exists in the organizedData, push the user
      if (organizedData[role.name]) {
        organizedData[role.name].push(item.user)
      } else {
        // If the role doesn't exist, create a new array with the user
        organizedData[role.name] = [item.user]
      }
    })

    // Check if there are additional roles
    if (item.add_roles) {
      item.add_roles.forEach(role => {
        // If the role exists in the organizedData, push the user
        if (organizedData[role.name]) {
          organizedData[role.name].push(item.user)
        } else {
          // If the role doesn't exist, create a new array with the user
          organizedData[role.name] = [item.user]
        }
      })
    }
  })

  return organizedData
})

onBeforeMount(() => emit('aside-visible', false))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>개요</h5>
    </CCol>

    <CCol class="text-right">
      <span class="mr-2 form-text">
        <v-icon icon="mdi-bookmark-multiple" color="primary" size="sm" />
        <router-link to="" class="ml-1">북마크 추가</router-link>
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
            <CDropdownItem class="form-text">
              <router-link :to="{ name: '프로젝트 - 추가', query: { parent: iProject?.pk } }">
                <v-icon icon="mdi-plus-circle" color="success" size="sm" />
                새 하위 프로젝트
              </router-link>
            </CDropdownItem>
            <CDropdownItem class="form-text">
              <router-link to="">
                <v-icon icon="mdi-lock" color="warning" size="sm" />
                닫기
              </router-link>
            </CDropdownItem>
            <CDropdownItem class="form-text">
              <router-link to="">
                <v-icon icon="mdi-trash-can-outline" color="danger" size="sm" />
                삭제
              </router-link>
            </CDropdownItem>
            <CDropdownItem class="form-text">
              <router-link to="">
                <v-icon icon="mdi-cog" color="secondary" size="sm" />
                설정
              </router-link>
            </CDropdownItem>
          </CDropdownMenu>
        </CDropdown>
      </span>
    </CCol>
  </CRow>

  <CRow class="mb-2">
    <CCol>{{ iProject?.description }}</CCol>
  </CRow>

  <CRow>
    <CCol lg="6">
      <CRow class="mb-3">
        <CCard :color="isDark ? '' : 'light'">
          <CCardBody>
            <CCardSubtitle>업무 추적</CCardSubtitle>
            <CTable bordered hover small striped class="mt-2 mb-0">
              <CTableHead>
                <CTableRow class="text-center">
                  <CTableHeaderCell scope="col"></CTableHeaderCell>
                  <CTableHeaderCell scope="col">진행중</CTableHeaderCell>
                  <CTableHeaderCell scope="col">완료됨</CTableHeaderCell>
                  <CTableHeaderCell scope="col">합계</CTableHeaderCell>
                </CTableRow>
              </CTableHead>

              <CTableBody>
                <CTableRow v-for="i in 3" :key="i" class="text-center">
                  <CTableHeaderCell>결함</CTableHeaderCell>
                  <CTableDataCell>0</CTableDataCell>
                  <CTableDataCell>0</CTableDataCell>
                  <CTableDataCell>0</CTableDataCell>
                </CTableRow>
              </CTableBody>
            </CTable>
          </CCardBody>

          <CCardText class="mx-3 mb-2"> 모든 업무 보기 | 요약 | 달력 | Gantt 차트</CCardText>
        </CCard>
      </CRow>

      <CRow class="mb-3">
        <CCard :color="isDark ? '' : 'light'">
          <CCardBody>
            <h6>
              <v-icon icon="mdi-clock-outline" size="small" />
              시간추적
            </h6>
            <ul class="pl-4 mb-0">
              <li>추정시간 : 48:00 시간</li>
              <li>소요시간 : 0:00 시간</li>
            </ul>
          </CCardBody>

          <CCardText class="mx-3 mb-2"> 작업시간 기록 | 자세히 | 보고서</CCardText>
        </CCard>
      </CRow>
    </CCol>

    <CCol lg="6">
      <CCard
        v-if="!!Object.keys(computedMembers).length"
        :color="isDark ? '' : 'light'"
        class="mb-3"
      >
        <CCardBody>
          <CCardSubtitle>구성원</CCardSubtitle>
          <CCardText>
            <div v-for="(val, key) in computedMembers" :key="key">
              {{ key }} :

              <span v-for="(u, i) in val" :key="u.pk">
                <router-link :to="{ name: '사용자 - 보기', params: { userId: u.pk } }">
                  {{ u.username }}
                </router-link>
                <span v-if="Number(i) + 1 < val.length">, </span>
              </span>
            </div>
          </CCardText>
        </CCardBody>
      </CCard>

      <CCard v-if="iProject?.sub_projects?.length" :color="isDark ? '' : 'light'" class="mb-3">
        <CCardBody>
          <CCardSubtitle>하위 프로젝트</CCardSubtitle>
          <CCardText>
            <router-link
              v-for="(sub, i) in iProject.sub_projects"
              :to="{ name: '(개요)', params: { projId: sub.slug } }"
              :key="sub.pk"
            >
              {{ sub.name }}<span v-if="i + 1 < iProject?.sub_projects?.length">, </span>
            </router-link>
          </CCardText>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
</template>
