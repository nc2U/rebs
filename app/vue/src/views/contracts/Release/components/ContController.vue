<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { useRouter } from 'vue-router'

const emit = defineEmits(['search-contractor', 'get-release'])

const search = ref('')

const contractStore = useContract()
const contractorList = computed(() => contractStore.contractorList)

const searchContractor = () => emit('search-contractor', search.value)

const router = useRouter()
const setContractor = (pk: number, release: number | null) => {
  router.push({ name: '계약해지 관리', query: { contractor: pk } })
  if (release !== null) emit('get-release', release)
  else contractStore.contRelease = null

  search.value = ''
  contractStore.contractorList = []
}
</script>

<template>
  <CCallout color="danger" class="pb-0 mb-4">
    <CRow>
      <CCol>
        <CRow>
          <CCol md="4" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="search"
                placeholder="계약자, 비고, 계약 일련번호"
                aria-label="Search"
                aria-describedby="addon-wrapping"
                @keydown.enter="searchContractor"
              />
              <CInputGroupText @click="searchContractor">
                계약 건 찾기
              </CInputGroupText>
            </CInputGroup>
          </CCol>
          <CCol
            v-if="contractorList && contractorList.length > 0"
            color="warning"
            class="p-1 pl-3 mb-2"
          >
            <CButton
              v-for="contractor in contractorList"
              :key="contractor.pk"
              type="button"
              color="dark"
              variant="outline"
              size="sm"
              @click="
                setContractor(contractor.pk, contractor.contractorrelease)
              "
            >
              {{ `${contractor.name}(${contractor.__str__})` }}
            </CButton>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <CRow>
      <!--      <CCol color="warning" class="p-2 pl-3" v-if="contractIndex.length !== 0">-->
      <!--        <CButton-->
      <!--          type="button"-->
      <!--          color="dark"-->
      <!--          v-for="cont in contractIndex"-->
      <!--          :key="cont.pk"-->
      <!--          @click="getContract(cont.pk)"-->
      <!--          variant="outline"-->
      <!--          size="sm"-->
      <!--        >-->
      <!--          {{ `${cont.contractor}(${cont.serial_number})` }}-->
      <!--        </CButton>-->
      <!--      </CCol>-->
      <!--      <CCol v-else class="mt-3 m-2" :class="textClass">-->
      <!--        {{ msg }}-->
      <!--      </CCol>-->
    </CRow>
  </CCallout>
</template>
