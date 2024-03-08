<script lang="ts" setup>
import { ref, computed, onBeforeMount, inject, type ComputedRef } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { useWork } from '@/store/pinia/work'
import type { IssueProject, SimpleMember } from '@/store/types/work'
import NoData from '@/views/_Work/components/NoData.vue'
import FormModal from '@/components/Modals/FormModal.vue'

const iProject = inject<ComputedRef<IssueProject>>('iProject')

// FormModal S ------------------
const memberFormModal = ref()

const validated = ref(false)

const users = ref([])
const roles = ref([])

const editMode = ref<number | null>(null)

const workStore = useWork()
const parentMembers = computed<SimpleMember[]>(() => workStore.issueProject?.parent_members ?? [])
const memberList = computed<SimpleMember[]>(() => workStore.issueProject?.members ?? [])

const computedMembers = computed(() => [...parentMembers.value, ...memberList.value])

const roleList = computed(() => workStore.roleList)
const patchIssueProject = (payload: { slug: string; users: number[]; roles: number[] }) =>
  workStore.patchIssueProject(payload)

const accStore = useAccount()
const userList = computed(() => {
  const memPkList = memberList.value.map(m => m.user.pk)
  // 전체 회원 중 이 프로젝트 구성원을 제외한 목록
  return accStore.usersList.filter(u => !memPkList.includes(u.pk as number))
})

const callModal = () => memberFormModal.value.callModal()

const onSubmit = (event: Event) => {
  const el = event.currentTarget as HTMLFormElement
  if (!el.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()
    validated.value = true
  } else {
    modalAction()
    validated.value = false
    memberFormModal.value.close()
  }
}

const modalAction = () => {
  const _memList = [...users.value.sort((a, b) => a - b)]
  const _roleList = [...roles.value.sort((a, b) => a - b)]
  patchIssueProject({ slug: iProject?.value.slug as string, users: _memList, roles: _roleList })
  users.value = []
  roles.value = []
}
// FormModal E ------------------

const memberRole = ref([]) // 업데이트할 멤버의 권한

const isInherit = (mem: number, pk: number) =>
  parentMembers.value
    .filter(m => m.pk === mem)[0]
    ?.roles.map(r => r.pk)
    .includes(pk)

const toEdit = (mem: any) => {
  console.log(mem)
  editMode.value = mem.pk
  memberRole.value = mem.roles.map((r: { pk: number; name: string }) => r.pk)
}

const cancelEdit = () => {
  editMode.value = null
  memberRole.value = []
}

const editSubmit = (pk: number, user: number) => {
  const parent = parentMembers.value.filter(m => m.pk === pk)[0]?.roles.map(r => r.pk)
  const slug = iProject?.value.slug as string

  if (parent) {
    // 멤버 정보 등록
    const roles = memberRole.value.filter(r => !parent.includes(r)) // 부모 권한 대비 추가 권한
    patchIssueProject({ slug, users: [user], roles })
  } else {
    // 멤버 정보 수정
    const roles = memberRole.value
    workStore.patchMember({ pk, roles, slug })
  }
  cancelEdit()
}

const toDelete = () => alert(iProject?.value.slug + ' - 삭제')

onBeforeMount(() => {
  accStore.fetchUsersList()
  workStore.fetchRoleList()
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link to="" class="ml-1" @click="callModal"> 새 구성원 </router-link>
      </span>
    </CCol>

    <CCol class="text-right">
      <span>
        <v-icon icon="mdi-cog" color="grey" size="sm" />
        <router-link :to="{ name: '사용자' }" class="ml-1">관리</router-link>
      </span>
    </CCol>
  </CRow>

  <NoData v-if="!computedMembers.length" />

  <CRow v-else>
    <CCol>
      <v-divider class="my-0" />
      <CTable hover small striped responsive>
        <colgroup>
          <col style="width: 5%" />
          <col style="width: 25%" />
          <col style="width: 45%" />
          <col style="width: 25%" />
        </colgroup>
        <CTableHead>
          <CTableRow class="text-center">
            <CTableHeaderCell scope="col"></CTableHeaderCell>
            <CTableHeaderCell scope="col">사용자</CTableHeaderCell>
            <CTableHeaderCell scope="col">역할</CTableHeaderCell>
            <CTableHeaderCell scope="col">비고</CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="mem in computedMembers" :key="mem.pk" align="middle">
            <CTableHeaderCell></CTableHeaderCell>
            <CTableDataCell>
              <router-link to="">{{ mem.user.username }}</router-link>
            </CTableDataCell>

            <CTableDataCell>
              <div v-if="editMode === mem.pk">
                <div v-for="role in roleList" :key="role.pk">
                  <CFormCheck
                    v-model="memberRole"
                    :label="role.name"
                    :value="role.pk"
                    :id="'role-' + role.pk"
                    :disabled="isInherit(mem.pk, role.pk)"
                    class="text-left"
                  />
                  <span v-if="isInherit(mem.pk, role.pk)" class="form-text">
                    상위 프로젝트로부터 상속
                  </span>
                </div>

                <CButton
                  color="success"
                  size="sm"
                  type="button"
                  class="mt-2"
                  @click="editSubmit(mem.pk, mem.user.pk)"
                >
                  저장
                </CButton>
                <CButton
                  color="secondary"
                  variant="outline"
                  size="sm"
                  type="button"
                  @click="cancelEdit"
                  class="mt-2"
                >
                  취소
                </CButton>
              </div>
              <div v-else>
                <span v-for="(mr, i) in mem.roles" :key="mr.pk">
                  {{ mr.name }}<span v-if="mem.roles.length > i + 1">, </span>
                </span>
              </div>
            </CTableDataCell>
            <CTableDataCell class="text-center">
              <span class="mr-2">
                <v-icon icon="mdi-pencil" color="amber" size="sm" />
                <router-link to="" @click="toEdit(mem)">편집</router-link>
              </span>
              <span>
                <v-icon icon="mdi-trash-can-outline" color="grey" size="sm" />
                <router-link to="" @click="toDelete">삭제</router-link>
              </span>
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
  </CRow>

  <FormModal ref="memberFormModal" size="xl">
    <template #icon></template>
    <template #header>새 구성원</template>
    <template #default>
      <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="onSubmit">
        <CModalBody class="text-body">
          <CCard class="mb-3">
            <CCardHeader>
              <v-icon icon="mdi-check" color="success" size="sm" />
              추가할 사용자 선택
            </CCardHeader>
            <CCardBody class="pb-5">
              <CFormCheck
                inline
                v-for="u in userList"
                :key="u.pk"
                :value="u.pk"
                :id="u.username"
                :label="u.username"
                v-model="users"
                :required="!users.length"
              />
            </CCardBody>
          </CCard>

          <CCard>
            <CCardHeader>
              <v-icon icon="mdi-check" color="success" size="sm" />
              역할
            </CCardHeader>
            <CCardBody>
              <CFormCheck
                inline
                v-for="r in roleList"
                :key="r.pk"
                :value="r.pk"
                :id="r.name"
                :label="r.name"
                v-model="roles"
                :required="!roles.length"
              />
            </CCardBody>
          </CCard>
        </CModalBody>
        <CModalFooter>
          <CButton color="light" @click="memberFormModal.close"> 닫기</CButton>
          <CButton color="primary" type="submit">추가</CButton>
        </CModalFooter>
      </CForm>
    </template>
  </FormModal>
</template>
