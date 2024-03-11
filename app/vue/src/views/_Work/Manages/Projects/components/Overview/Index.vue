<script lang="ts" setup>
import { computed, inject, onBeforeMount } from 'vue'
import { useWork } from '@/store/pinia/work'
import type { SimpleMember } from '@/store/types/work'

const emit = defineEmits(['aside-visible'])

const isDark = inject('isDark')

const workStore = useWork()
const iProject = computed(() => workStore.issueProject)

const parentMembers = computed<SimpleMember[]>(() => workStore.issueProject?.parent_members ?? [])
const memberList = computed<SimpleMember[]>(() => workStore.issueProject?.members ?? [])

const computedMembers = computed(() => {
  // 부모멤버권한 + 하위멤버권한 = 멤버 목록 합치기
  // 1. 부모유저와 동일한 member가 있는 경우 멤버 역할(roles)을 부모 역할에 Merge
  const computedParents = parentMembers.value.map(pm => {
    const existMembers = memberList.value.filter(m =>
      parentMembers.value.map(pm => pm.user.pk).includes(m.user.pk),
    )

    if (existMembers.map(e => e.user.pk).includes(pm.user.pk)) {
      // 부모유저와 하위멤버 유저가 동일한 경우
      pm.add_roles = existMembers.filter(e => e.user.pk === pm.user.pk)[0].roles
      return pm
    } else return pm
  })

  // 2. 부모유저와 동일한 member가 있는 경우 해당 멤버는 제외 한 나머지를 부모 멤버와 Merge
  const computedMembers = memberList.value.filter(
    m => !parentMembers.value.map(pm => pm.user.pk).includes(m.user.pk),
  )

  const mergedMembers = [...computedParents, ...computedMembers]

  const organizedData = {}

  mergedMembers.forEach(item => {
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

  return organizedData as { [key: string]: Array<{ pk: number; username: string }> }
})

onBeforeMount(() => emit('aside-visible', false))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>개요</h5>
    </CCol>

    <CCol class="text-right">
      <span class="mr-2">
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
            <CDropdownItem>
              <router-link :to="{ name: '프로젝트 - 생성', query: { parent: iProject?.pk } }">
                <v-icon icon="mdi-plus-circle" color="success" size="sm" />
                새 하위 프로젝트
              </router-link>
            </CDropdownItem>
            <CDropdownItem>
              <router-link to="">
                <v-icon icon="mdi-lock" color="warning" size="sm" />
                닫기
              </router-link>
            </CDropdownItem>
            <CDropdownItem>
              <router-link to="">
                <v-icon icon="mdi-trash-can-outline" color="danger" size="sm" />
                삭제
              </router-link>
            </CDropdownItem>
            <CDropdownItem>
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
                <router-link to="">
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

  <CRow>
    <CCol>{{ iProject }}</CCol>
  </CRow>
</template>
