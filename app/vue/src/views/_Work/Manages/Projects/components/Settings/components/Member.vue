<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { useAccount } from '@/store/pinia/account'
import NoData from '@/views/_Work/components/NoData.vue'
import FormModal from '@/components/Modals/FormModal.vue'

const memberFormModal = ref()

const memberList = computed(() => [])

const callModal = () => memberFormModal.value.callModal()

const accStore = useAccount()
const userList = computed(() => accStore.usersList)

onBeforeMount(() => accStore.fetchUsersList())
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

  <NoData v-if="!memberList.length" />

  <CRow v-else>
    <CCol>
      <v-divider class="my-0" />
      <CTable hover small striped responsive>
        <CTableHead>
          <CTableRow class="text-center">
            <CTableHeaderCell scope="col"></CTableHeaderCell>
            <CTableHeaderCell scope="col">사용자/그룹</CTableHeaderCell>
            <CTableHeaderCell scope="col">역할</CTableHeaderCell>
            <CTableHeaderCell scope="col"></CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="i in 2" :key="i" class="text-center">
            <CTableHeaderCell></CTableHeaderCell>
            <CTableDataCell>
              <router-link to="">austin1 kho</router-link>
            </CTableDataCell>
            <CTableDataCell> 관리자, 개발자</CTableDataCell>
            <CTableDataCell>
              <span class="mr-2">
                <v-icon icon="mdi-pencil" color="amber" size="sm" />
                <router-link to="">편집</router-link>
              </span>
              <span>
                <v-icon icon="mdi-trash-can-outline" color="grey" size="sm" />
                <router-link to="">삭제</router-link>
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
      <CModalBody class="text-body">
        <CCard class="mb-3">
          <CCardHeader>
            <v-icon icon="mdi-check" color="success" size="sm" />
            추가할 사용자 선택
          </CCardHeader>
          <CCardBody>
            <CFormCheck
              v-for="u in userList"
              :key="u.pk"
              inline
              :id="'user' + u.pk"
              :label="u.username"
            />
          </CCardBody>
        </CCard>

        <CCard>
          <CCardHeader>
            <v-icon icon="mdi-check" color="success" size="sm" />
            역할
          </CCardHeader>
          <CCardBody>
            <CFormCheck inline id="id1" label="관리자" />
            <CFormCheck inline id="id2" label="개발자" />
            <CFormCheck inline id="id3" label="보고자" />
          </CCardBody>
        </CCard>
      </CModalBody>
      <CModalFooter>
        <CButton color="light" @click="memberFormModal.close"> 닫기</CButton>
        <CButton color="primary">추가</CButton>
      </CModalFooter>
    </template>
  </FormModal>
</template>
